from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
import os
import logging
import threading
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from .model import ModelWrapper

app = FastAPI(title="Proverbs Generator API")

# Config
model_name = os.environ.get("MODEL_NAME", "gpt2")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "info").lower()

# lazy model
_model_lock = threading.RLock()
_model_instance: Optional[ModelWrapper] = None

# shared executor
_shared_executor: Optional[ThreadPoolExecutor] = None


def get_model() -> ModelWrapper:
    global _model_instance
    if _model_instance is None:
        with _model_lock:
            if _model_instance is None:
                _model_instance = ModelWrapper(model_name)
    return _model_instance


def _check_admin_auth(request: Request):
    admin_key = os.environ.get("ADMIN_API_KEY")
    if not admin_key:
        raise HTTPException(status_code=404, detail="admin endpoint disabled")
    token = request.headers.get("x-admin-token")
    if token != admin_key:
        raise HTTPException(status_code=403, detail="admin auth failed")


def _run_in_background(fn, *args, **kwargs):
    t = threading.Thread(target=fn, args=args, kwargs=kwargs, daemon=True)
    t.start()
    return t


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _shared_executor
    _shared_executor = ThreadPoolExecutor(max_workers=2)
    try:
        yield
    finally:
        if _shared_executor is not None:
            _shared_executor.shutdown(wait=False)


app.router.lifespan_context = lifespan

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("CORS_ALLOW_ORIGIN", "*")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def _request_logging_middleware(request: Request, call_next):
    if LOG_LEVEL in ("debug", "info"):
        logger = logging.getLogger("uvicorn.access")
        logger.info(f"{request.method} {request.url}")
    response = await call_next(request)
    if LOG_LEVEL == "debug":
        logger = logging.getLogger("uvicorn.access")
        logger.info(f"{request.method} {request.url} -> {response.status_code}")
    return response


@app.post('/admin/load_real')
async def admin_load_real(request: Request, model_name: Optional[str] = None):
    _check_admin_auth(request)
    try:
        m = get_model()
    except Exception:
        raise HTTPException(status_code=500, detail='model container unavailable')

    _run_in_background(m.load_real_model, model_name)
    return {"status": "accepted", "action": "loading_real_model"}


@app.post('/admin/unload')
async def admin_unload(request: Request):
    _check_admin_auth(request)
    try:
        m = get_model()
    except Exception:
        raise HTTPException(status_code=500, detail='model container unavailable')

    _run_in_background(m.unload_model)
    return {"status": "accepted", "action": "unloading_model"}


@app.get("/admin/status")
async def admin_status(request: Request):
    _check_admin_auth(request)
    try:
        model = get_model()
    except Exception:
        raise HTTPException(status_code=500, detail='model container unavailable')
    try:
        return model.status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/ready")
async def ready():
    try:
        m = get_model()
    except Exception:
        return {"ready": False}
    ready_flag = getattr(m, "_ready", True)
    return {"ready": bool(ready_flag)}


class GenerateRequest(BaseModel):
    prompt: str
    max_new_tokens: Optional[int] = 50


class GenerateResponse(BaseModel):
    generated_text: str


@app.get("/health")
async def health():
    return {"status": "ok", "model": model_name}


@app.post("/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest):
    if not req.prompt:
        raise HTTPException(status_code=400, detail="prompt is required")
    try:
        model = get_model()
        if not getattr(model, "_ready", True):
            raise HTTPException(status_code=503, detail="model not ready")

        timeout_seconds = int(os.environ.get("MODEL_GEN_TIMEOUT", "30"))

        def run_gen():
            return model.generate(req.prompt, max_new_tokens=req.max_new_tokens)

        global _shared_executor
        if _shared_executor is None:
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                fut = executor.submit(run_gen)
                try:
                    text = fut.result(timeout=timeout_seconds)
                except concurrent.futures.TimeoutError:
                    fut.cancel()
                    raise HTTPException(status_code=504, detail="generation timeout")
        else:
            fut = _shared_executor.submit(run_gen)
            try:
                text = fut.result(timeout=timeout_seconds)
            except concurrent.futures.TimeoutError:
                fut.cancel()
                raise HTTPException(status_code=504, detail="generation timeout")

        return GenerateResponse(generated_text=text)
    except HTTPException:
        raise
    except Exception as e:
        logging.exception("Generation error")
        raise HTTPException(status_code=500, detail=str(e))
 

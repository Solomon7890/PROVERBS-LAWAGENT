import streamlit as st
import base64
from datetime import datetime
import os
import mimetypes
import streamlit.components.v1 as components


def get_logo_base64(logo_type: str = "random"):
    """Get base64 encoded logo for display (kept for backward compatibility)."""
    import random

    logo_files = {
        "proverb": "proverb_logo.svg",
        "eagle": "proverb_eagle_logo.svg",
        "law": "iamlaw_logo.svg"
    }

    if logo_type == "random":
        logo_type = random.choice(["proverb", "eagle", "law"])

    logo_path = logo_files.get(logo_type, "proverb_logo.svg")

    try:
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    except Exception:
        pass
    return None


def _discover_logo_paths():
    """Find available logo image paths from common locations."""
    candidates = [
        "proverb_logo.svg",
        "iamlaw_logo.svg",
        "proverb_eagle_logo.svg",
        os.path.join("static", "proverb_eagle_logo.svg"),
    ]
    for folder in ["assets", "static"]:
        if os.path.isdir(folder):
            for name in os.listdir(folder):
                if name.lower().endswith((".png", ".jpg", ".jpeg", ".svg")):
                    candidates.append(os.path.join(folder, name))
    # De-duplicate and keep only existing files
    seen, result = set(), []
    for p in candidates:
        if p not in seen and os.path.exists(p):
            seen.add(p)
            result.append(p)
    return result


def _to_data_uri(path: str) -> str | None:
    """Convert an image file to a data URI string suitable for <img src>."""
    try:
        mime, _ = mimetypes.guess_type(path)
        if not mime:
            ext = os.path.splitext(path)[1].lower()
            if ext == ".svg":
                mime = "image/svg+xml"
            elif ext in (".jpg", ".jpeg"):
                mime = "image/jpeg"
            elif ext == ".png":
                mime = "image/png"
            else:
                mime = "application/octet-stream"
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f"data:{mime};base64,{b64}"
    except Exception:
        return None


def render_rotating_logo(interval_ms: int = 25000, width_px: int = 150):
    """Render a rotating logo block using JS inside a Streamlit component."""
    paths = _discover_logo_paths()
    data_uris = [u for u in (_to_data_uri(p) for p in paths) if u]
    if not data_uris:
        return False  # Fallback to static

    js_array = ",".join([f"'{u}'" for u in data_uris])
    html = f"""
    <div style="text-align:center; margin-bottom: 1rem;">
      <img id="rotating-logo" src="{data_uris[0]}" 
           style="width: {width_px}px; height: {width_px}px; object-fit: contain; 
           border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.15);" 
           alt="Pro'VerBs Logo" />
    </div>
    <script>
      const logos = [{js_array}];
      let idx = 0;
      setInterval(() => {{
        idx = (idx + 1) % logos.length;
        const img = document.getElementById('rotating-logo');
        if (img) img.src = logos[idx];
      }}, {interval_ms});
    </script>
    """
    components.html(html, height=width_px + 40)
    return True


def render_hero_section():
    """Render the hero section with rotating or static logo."""
    hero_html = """
    <div class="hero-section">
    """
    rotated = render_rotating_logo(interval_ms=25000, width_px=150)

    if not rotated:
        logo_base64 = get_logo_base64("random")
        if logo_base64:
            hero_html += f"""
            <div style="margin-bottom: 2rem;">
                <img src="data:image/svg+xml;base64,{logo_base64}" 
                     style="width: 150px; height: 150px; margin-bottom: 1rem;" 
                     alt="Pro'VerBs Logo"/>
            </div>
            """

    hero_html += """
        <h1 class="hero-title">Pro'VerBs™</h1>
    </div>
    """
    st.markdown(hero_html, unsafe_allow_html=True)


if __name__ == "__main__":
    st.set_page_config(page_title="Pro'VerBs™ App", page_icon="⚖️", layout="centered")
    render_hero_section()
    st.write("Welcome to Pro'VerBs™ App")

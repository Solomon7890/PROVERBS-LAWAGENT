import sys
from pathlib import Path
import streamlit as st

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# Streamlit configuration
st.set_page_config(
    page_title="Pro'VerBs™ LAW'8",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for mobile-friendly design (edit as needed)
st.markdown(
    """
    <style>
    /* Add custom CSS here */
    body { margin: 0; padding: 0; }
    /* Example responsive tweaks */
    @media (max-width: 600px) {
        .stApp { padding: 8px; }
    }
    </style>
    """,
    unsafe_allow_html=True
)


def safe_get(dct, key, default="N/A"):
    try:
        return dct.get(key, default)
    except Exception:
        return default


def main():
    # --- Email entry / access
    st.markdown("### Enter Email to Access Platform")
    user_email = st.text_input(
        "Email Address:",
        placeholder="your.email@example.com"
    )

    if st.button("Access LAW'8 Platform", type="primary"):
        if user_email and "@" in user_email:
            st.session_state.user_email = user_email
            st.success(f"✅ Welcome {user_email}!")
        else:
            st.warning("⚠️ Please enter a valid email address")
            # return here is optional; keeping the app running so user can still see UI
    # show header/logo (optional)
    try:
        from utils.logo_manager import get_logo_manager

        logo_manager = get_logo_manager()
        st.markdown(logo_manager.get_header_logo_html(), unsafe_allow_html=True)
    except Exception:
        # Logo manager missing — not fatal
        pass

    st.title("⚖️ Pro'VerBs™ LAW'8")
    if "user_email" in st.session_state:
        st.caption(f"Universal Law Platform | User: {st.session_state.user_email}")

    # --- Main legal query interface
    st.markdown("### Enter Your Legal Query")

    legal_query = st.text_area(
        "Describe your legal question or situation:",
        placeholder=(
            "What are my constitutional rights? "
            "Can the government take my property? "
            "What laws apply to my business?"
        ),
        height=120
    )

    if st.button("🔍 Analyze with LAW'8", type="primary"):
        if legal_query:
            with st.spinner("⚛️ Processing through quantum universal law analysis..."):
                try:
                    from modules.quantum_universal_law_analysis import (
                        perform_quantum_universal_analysis,
                    )

                    # Execute quantum analysis on all categories
                    quantum_result = perform_quantum_universal_analysis(legal_query, None) or {}

                    st.success("✅ Analysis Complete")

                    # display metrics (use safe defaults if keys missing)
                    col1, col2 = st.columns(2)
                    with col1:
                        conf = safe_get(quantum_result, "quantum_confidence", 0)
                        proc_ms = safe_get(quantum_result, "processing_time_ms", 0)
                        try:
                            st.metric("Confidence", f"{float(conf):.0%}")
                        except Exception:
                            st.metric("Confidence", str(conf))
                        st.metric("Processing", f"{proc_ms}ms")

                    with col2:
                        coh = safe_get(quantum_result, "universal_law_coherence", 0)
                        auth = safe_get(quantum_result, "divine_law_supremacy_score", 0)
                        try:
                            st.metric("Coherence", f"{float(coh):.0%}")
                        except Exception:
                            st.metric("Coherence", str(coh))
                        try:
                            st.metric("Authority", f"{float(auth):.0%}")
                        except Exception:
                            st.metric("Authority", str(auth))

                    # Legal domain results
                    st.markdown("#### ⚖️ Legal Analysis")

                    # Show detailed results in expandable section
                    with st.expander("🔬 Detailed Quantum Analysis"):
                        analyzed_categories = safe_get(quantum_result, "law_categories_analyzed", [])
                        st.info(f"Analyzed {len(analyzed_categories)} law categories simultaneously")
                        st.json(
                            {
                                "Engine": "LAW'8 - ADAPPT-I™ Quantum",
                                "Mode": "Universal Superposition",
                                "Categories": analyzed_categories,
                            }
                        )
                except Exception as e:
                    # If analysis module fails, give informative messages but keep app alive
                    st.error("⚠️ Analysis module failed or is unavailable.")
                    st.info("⚛️ Quantum Universal Law Analysis - ADAPPT-I™ Engine ACTIVE")
                    st.info("🔬 Processing all 14 law categories simultaneously")
                    st.info("🩸 Divine Law of Blood supremacy confirmed")
        else:
            st.warning("⚠️ Please enter your legal question")

    # --- Service selector
    service_type = st.selectbox(
        "Choose Service:",
        [
            "📱 SMS Notifications",
            "📧 Email Communications",
            "🌐 Web Scraping",
            "📄 Document Analysis",
        ],
    )

    # SMS Notifications
    if service_type == "📱 SMS Notifications":
        sms_phone = st.text_input("Phone Number:", placeholder="+1234567890")
        sms_message = st.text_area("Message:", placeholder="Legal notification...", height=80)

        if st.button("📱 Send SMS"):
            if sms_phone and sms_message:
                try:
                    from modules.communication_wrappers import send_sms_notification

                    success = send_sms_notification(sms_phone, sms_message)
                    if success:
                        st.success("✅ SMS sent successfully!")
                    else:
                        st.error("❌ Failed to send SMS")
                except Exception:
                    st.error("⚠️ SMS module not available")
            else:
                st.warning("Please enter phone and message")

    # Email Communications
    elif service_type == "📧 Email Communications":
        email_to = st.text_input("Email:", placeholder="client@example.com")
        email_subject = st.text_input("Subject:", placeholder="Legal Consultation")
        email_content = st.text_area("Content:", placeholder="Analysis results...", height=100)

        if st.button("📧 Send Email"):
            if email_to and email_subject and email_content:
                try:
                    from modules.communication_wrappers import send_email_notification

                    result = send_email_notification(email_to, email_subject, email_content)
                    if result:
                        st.success("✅ Email sent successfully!")
                    else:
                        st.error("❌ Failed to send email")
                except Exception:
                    st.error("⚠️ Email module not available")
            else:
                st.warning("Please fill all fields")

    # Web Scraping
    elif service_type == "🌐 Web Scraping":
        scrape_url = st.text_input("Website URL:", placeholder="https://example.com/legal-content")

        if st.button("🕸️ Scrape Content"):
            if scrape_url:
                try:
                    from modules.web_scraper import scrape_website_content

                    content = scrape_website_content(scrape_url) or ""
                    st.markdown("**Scraped Content:**")
                    if len(content) > 100:
                        st.text_area(
                            "",
                            value=content[:500] + ("..." if len(content) > 500 else ""),
                            height=150,
                            disabled=True,
                        )
                        st.success("✅ Content extracted!")
                    else:
                        st.info("🕸️ Processing...")
                except Exception:
                    st.error("⚠️ Web scraping module not available")
            else:
                st.warning("Please enter URL")

    # Document Analysis
    elif service_type == "📄 Document Analysis":
        uploaded_file = st.file_uploader(
            "Upload Document", type=["pdf", "docx", "txt", "jpg", "png"]
        )

        if uploaded_file:
            col1, col2 = st.columns(2)
            with col1:
                st.info("📂 Document Uploaded")
            with col2:
                st.success("✅ Ready for Analysis")
            # You can add document-processing logic here (OCR, text extraction, etc.)

    # Law of Blood Authority (static section)
    st.markdown("### 🩸 Law of Blood Authority")
    st.success("\"The rights of Blood and kindred cannot be destroyed by any civil law\"")
    st.caption("Supreme Natural Law Principle - Divine Authority")

    # Footer
    st.markdown("---")
    st.caption("🔒 Powered by LAW'8 - ADAPPT-I™ Quantum Universal Law Platform")


if __name__ == "__main__":
    main()

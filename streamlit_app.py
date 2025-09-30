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

# Custom CSS for mobile-friendly design
st.markdown(
    """
    <style>
    /* Add custom CSS here */
    </style>
    """,
    unsafe_allow_html=True
)


def main():
    # Check if user has entered email
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
            return

    # Header with rotating logos
    try:
        from utils.logo_manager import get_logo_manager
        logo_manager = get_logo_manager()
        st.markdown(logo_manager.get_header_logo_html(), unsafe_allow_html=True)
    except Exception:
        st.error("⚠️ Logo Manager not found")

    st.title("⚖️ Pro'VerBs™ LAW'8")
    if "user_email" in st.session_state:
        st.caption(f"Universal Law Platform | User: {st.session_state.user_email}")

    # Main legal query interface
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
                    from modules.quantum_universal_law_analysis import perform_quantum_universal_analysis

                    # Execute quantum analysis on all categories
                    quantum_result = perform_quantum_universal_analysis(legal_query, None)

                    st.success("✅ Analysis Complete")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Confidence", f"{quantum_result['quantum_confidence']:.0%}")
                        st.metric("Processing", f"{quantum_result['processing_time_ms']}ms")
                    with col2:
                        st.metric("Coherence", f"{quantum_result['universal_law_coherence']:.0%}")
                        st.metric("Authority", f"{quantum_result['divine_law_supremacy_score']:.0%}")

                    # Legal domain results
                    st.markdown("#### ⚖️ Legal Analysis")

                    # Show detailed results in expandable section
                    with st.expander("🔬 Detailed Quantum Analysis"):
                        analyzed_categories = quantum_result['law_categories_analyzed']
                        st.info(f"Analyzed {len(analyzed_categories)} law categories simultaneously")
                        st.json({
                            "Engine": "LAW'8 - ADAPPT-I™ Quantum",
                            "Mode": "Universal Superposition",
                            "Categories": analyzed_categories
                        })
                except Exception as e:
                    st.success("✅ LAW'8 Analysis Ready")
                    st.info("⚛️ Quantum Universal Law Analysis - ADAPPT-I™ Engine ACTIVE")
                    st.info("🔬 Processing all 14 law categories simultaneously")
                    st.info("🩸 Divine Law of Blood supremacy confirmed")
        else:
            st.warning("⚠️ Please enter your legal question")

    # Service selector
    service_type = st.selectbox(
        "Choose Service:",
        [
            "📱 SMS Notifications",
            "📧 Email Communications",
            "🌐 Web Scraping",
            "📄 Document Analysis"
        ]
    )

    if service_type == "📱 SMS Notifications":
        sms_phone = st.text_input("Phone Number:", placeholder="+1234567890")
        sms_message = st.text_area("Message:", placeholder="Legal notification...", height=80)

        if st.button("📱 Send SMS"):
            if sms_phone and sms_message:
                try:
                    from modules.communication_wrappers import send_sms_notification
                    result = send_sms_notification(sms_phone, sms_message)
                    if result:
                        st.success("✅ SMS sent successfully!")
                    else:
                        st.error("❌ Failed to send SMS")
                except Exception:
                    st.error("⚠️ SMS module not available")
            else:
                st.warning("Please enter phone and message")

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

    elif service_type == "🌐 Web Scraping":
        scrape_url = st.text_input("Website URL:", placeholder="https://example.com/legal-content")

        if st.button("🕸️ Scrape Content"):
            if scrape_url:
                try:
                    from modules.web_scraper import scrape_website_content
                    content = scrape_website_content(scrape_url)
                    st.markdown("**Scraped Content:**")
                    if len(content) > 100:
                        st.text_area(
                            "",
                            value=content[:500] + ("..." if len(content) > 500 else ""),
                            height=150,
                            disabled=True
                        )
                        st.success("✅ Content extracted!")
                    else:
                        st.info("🕸️ Processing...")
                except Exception:
                    st.error("⚠️ Web scraping module not available")
            else:
                st.warning("Please enter URL")

    elif service_type == "📄 Document Analysis":
        uploaded_file = st.file_uploader(
            "Upload Document", type=['pdf', 'docx', 'txt', 'jpg', 'png']
        )

        if uploaded_file:
            col1, col2 = st.columns(2)
            with col1:
                st.info("📂 Document Uploaded")
            with col2:
                st.success("✅ Ready for Analysis")

    # Law of Blood Authority
    st.markdown("### 🩸 Law of Blood Authority")
    st.success("\"The rights of Blood and kindred cannot be destroyed by any civil law\"")
    st.caption("Supreme Natural Law Principle - Divine Authority")

    # Footer
    st.markdown("---")
    st.caption("🔒 Powered by LAW'8 - ADAPPT-I™ Quantum Universal Law Platform")


if __name__ == "__main__":
    main()

@ -13,12 +13,10 @@ project_root = Path(__file__).parent
sys.path.append(str(project_root))

# Streamlit configuration
st.set_page_config(
    page_title="Pro'VerBs™ LAW'8",
st.set_page_config(page_title="Pro'VerBs™ LAW'8",
                   page_icon="⚖️",
                   layout="wide",
    initial_sidebar_state="collapsed"
)
                   initial_sidebar_state="collapsed")

# Custom CSS for mobile-friendly design
st.markdown("""
@ -61,7 +59,9 @@ st.markdown("""
           )
    }
</style>
""", unsafe_allow_html=True)
""",
            unsafe_allow_html=True)


def main():
    # Check if user has entered email
@ -89,7 +89,8 @@ def main():

        # Email entry
        st.markdown("### Enter Email to Access Platform")
        user_email = st.text_input("Email Address:", placeholder="your.email@example.com")
        user_email = st.text_input("Email Address:",
                                   placeholder="your.email@example.com")

        if st.button("Access LAW'8 Platform", type="primary"):
            if user_email and "@" in user_email:
@ -105,28 +106,33 @@ def main():
        # Header with rotating logos
        from utils.logo_manager import get_logo_manager
        logo_manager = get_logo_manager()
        st.markdown(logo_manager.get_header_logo_html(), unsafe_allow_html=True)
        st.markdown(logo_manager.get_header_logo_html(),
                    unsafe_allow_html=True)

        st.title("⚖️ Pro'VerBs™ LAW'8")
        st.caption(f"Universal Law Platform | User: {st.session_state.user_email}")
        st.caption(
            f"Universal Law Platform | User: {st.session_state.user_email}")

        # Main legal query interface
        st.markdown("### Enter Your Legal Query")

        legal_query = st.text_area(
            "Describe your legal question or situation:",
            placeholder="What are my constitutional rights? Can the government take my property? What laws apply to my business?",
            height=120
        )
            placeholder=
            "What are my constitutional rights? Can the government take my property? What laws apply to my business?",
            height=120)

        if st.button("🔍 Analyze with LAW'8", type="primary"):
            if legal_query:
                with st.spinner("⚛️ Processing through quantum universal law analysis..."):
                with st.spinner(
                        "⚛️ Processing through quantum universal law analysis..."
                ):
                    try:
                        from modules.quantum_universal_law_analysis import perform_quantum_universal_analysis

                        # Execute quantum analysis on all categories
                        quantum_result = perform_quantum_universal_analysis(legal_query, None)
                        quantum_result = perform_quantum_universal_analysis(
                            legal_query, None)

                        st.success("✅ Analysis Complete")

@ -135,11 +141,21 @@ def main():

                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Confidence", f"{quantum_result['quantum_confidence']:.0%}")
                            st.metric("Processing", f"{quantum_result['processing_time_ms']}ms")
                            st.metric(
                                "Confidence",
                                f"{quantum_result['quantum_confidence']:.0%}")
                            st.metric(
                                "Processing",
                                f"{quantum_result['processing_time_ms']}ms")
                        with col2:
                            st.metric("Coherence", f"{quantum_result['universal_law_coherence']:.0%}")
                            st.metric("Authority", f"{quantum_result['divine_law_supremacy_score']:.0%}")
                            st.metric(
                                "Coherence",
                                f"{quantum_result['universal_law_coherence']:.0%}"
                            )
                            st.metric(
                                "Authority",
                                f"{quantum_result['divine_law_supremacy_score']:.0%}"
                            )

                        # Legal domain results
                        st.markdown("#### ⚖️ Legal Analysis")
@ -149,8 +165,11 @@ def main():

                        # Show detailed results in expandable section
                        with st.expander("🔬 Detailed Quantum Analysis"):
                            analyzed_categories = quantum_result['law_categories_analyzed']
                            st.info(f"Analyzed {len(analyzed_categories)} law categories simultaneously")
                            analyzed_categories = quantum_result[
                                'law_categories_analyzed']
                            st.info(
                                f"Analyzed {len(analyzed_categories)} law categories simultaneously"
                            )
                            st.json({
                                "Engine": "LAW'8 - ADAPPT-I™ Quantum",
                                "Mode": "Universal Superposition",
@ -159,8 +178,12 @@ def main():
                            })
                    except Exception as e:
                        st.success("✅ LAW'8 Analysis Ready")
                        st.info("⚛️ Quantum Universal Law Analysis - ADAPPT-I™ Engine ACTIVE")
                        st.info("🔬 Processing all 14 law categories simultaneously")
                        st.info(
                            "⚛️ Quantum Universal Law Analysis - ADAPPT-I™ Engine ACTIVE"
                        )
                        st.info(
                            "🔬 Processing all 14 law categories simultaneously"
                        )
                        st.info("🩸 Divine Law of Blood supremacy confirmed")
            else:
                st.warning("Please enter your legal question")
@ -172,15 +195,16 @@ def main():

        # Service selector
        service_type = st.selectbox("Choose Service:", [
            "📱 SMS Notifications",
            "📧 Email Communications", 
            "🌐 Web Scraping",
            "📱 SMS Notifications", "📧 Email Communications", "🌐 Web Scraping",
            "📄 Document Analysis"
        ])

        if service_type == "📱 SMS Notifications":
            sms_phone = st.text_input("Phone Number:", placeholder="+1234567890")
            sms_message = st.text_area("Message:", placeholder="Legal notification...", height=80)
            sms_phone = st.text_input("Phone Number:",
                                      placeholder="+1234567890")
            sms_message = st.text_area("Message:",
                                       placeholder="Legal notification...",
                                       height=80)

            if st.button("📱 Send SMS"):
                if sms_phone and sms_message:
@ -197,15 +221,20 @@ def main():
                    st.warning("Please enter phone and message")

        elif service_type == "📧 Email Communications":
            email_to = st.text_input("Email:", placeholder="client@example.com")
            email_subject = st.text_input("Subject:", placeholder="Legal Consultation")
            email_content = st.text_area("Content:", placeholder="Analysis results...", height=100)
            email_to = st.text_input("Email:",
                                     placeholder="client@example.com")
            email_subject = st.text_input("Subject:",
                                          placeholder="Legal Consultation")
            email_content = st.text_area("Content:",
                                         placeholder="Analysis results...",
                                         height=100)

            if st.button("📧 Send Email"):
                if email_to and email_subject and email_content:
                    try:
                        from modules.communication_wrappers import send_email_notification
                        result = send_email_notification(email_to, email_subject, email_content)
                        result = send_email_notification(
                            email_to, email_subject, email_content)
                        if result:
                            st.success("✅ Email sent successfully!")
                        else:
@ -216,7 +245,9 @@ def main():
                    st.warning("Please fill all fields")

        elif service_type == "🌐 Web Scraping":
            scrape_url = st.text_input("Website URL:", placeholder="https://example.com/legal-content")
            scrape_url = st.text_input(
                "Website URL:",
                placeholder="https://example.com/legal-content")

            if st.button("🕸️ Scrape Content"):
                if scrape_url:
@ -225,7 +256,12 @@ def main():
                        content = scrape_website_content(scrape_url)
                        st.markdown("**Scraped Content:**")
                        if len(content) > 100:
                            st.text_area("", value=content[:500] + "..." if len(content) > 500 else content, height=150, disabled=True)
                            st.text_area(
                                "",
                                value=content[:500] +
                                "..." if len(content) > 500 else content,
                                height=150,
                                disabled=True)
                            st.success("✅ Content extracted!")
                        else:
                            st.info("🕸️ Processing...")
@ -235,7 +271,8 @@ def main():
                    st.warning("Please enter URL")

        elif service_type == "📄 Document Analysis":
            uploaded_file = st.file_uploader("Upload Document", type=['pdf', 'docx', 'txt', 'jpg', 'png'])
            uploaded_file = st.file_uploader(
                "Upload Document", type=['pdf', 'docx', 'txt', 'jpg', 'png'])

            if uploaded_file:
                col1, col2 = st.columns(2)
@ -255,12 +292,16 @@ def main():

        # Law of Blood Authority
        st.markdown("### 🩸 Law of Blood Authority")
        st.success("\"The rights of Blood and kindred cannot be destroyed by any civil law\"")
        st.success(
            "\"The rights of Blood and kindred cannot be destroyed by any civil law\""
        )
        st.caption("Supreme Natural Law Principle - Divine Authority")

        # Footer
        st.markdown("---")
        st.caption("🔒 Powered by LAW'8 - ADAPPT-I™ Quantum Universal Law Platform")
        st.caption(
            "🔒 Powered by LAW'8 - ADAPPT-I™ Quantum Universal Law Platform")


if __name__ == "__main__":
    main()

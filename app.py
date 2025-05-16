import streamlit as st
from pdf_utils import extract_text_from_pdf
from summarizer import summarize_text
from email_utils import send_email

st.set_page_config(page_title="PDF Summarizer", layout="centered")
st.title("📄 Summarize Any PDF using ChatGPT")

# Initialize session state for text and summary
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""

# Upload and extract PDF
uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting text..."):
        st.session_state.extracted_text = extract_text_from_pdf(uploaded_file)

    st.subheader("Extracted Text Preview")
    st.text(st.session_state.extracted_text[:1000] + '...')

    # Summarize Button
    if st.button("Summarize"):
        with st.spinner("Summarizing..."):
            st.session_state.summary = summarize_text(st.session_state.extracted_text)

# If summary is available, show options
if st.session_state.summary:
    st.subheader("📌 Summary")
    st.success(st.session_state.summary)

    # ✅ Download Button
    st.download_button(
        label="📥 Download Summary as .txt",
        data=st.session_state.summary,
        file_name="summary.txt",
        mime="text/plain"
    )

    # ✅ Email Section
    st.markdown("---")
    st.subheader("📧 Email the Summary")

    user_email = st.text_input("Enter your email address")

    if st.button("Send Summary via Email"):
        if user_email and "@" in user_email:
            success = send_email(user_email, st.session_state.summary)
            if success:
                st.success(f"✅ Summary sent to {user_email}")
            else:
                st.error("❌ Failed to send email. Check configuration.")
        else:
            st.warning("Please enter a valid email address.")

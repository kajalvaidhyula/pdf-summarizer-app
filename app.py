import streamlit as st
import os
from summarizer import summarize_text
from pdf_utils import extract_text_from_pdf
from email_utils import send_email

# --- Page Config ---
st.set_page_config(page_title="Smart Summary", page_icon="📄", layout="centered")

# --- Title / Description ---
st.markdown("""
    <h1 style='text-align: center; font-size: 48px;'>📄 Smart Summary</h1>
    <p style='text-align: center; font-size: 20px; color: #666;'>
        Upload your PDF. Get a human-friendly summary in seconds.<br>
        Powered by ChatGPT — simplified, cleaned, and delivered.
    </p>
""", unsafe_allow_html=True)

st.markdown("---")

# --- File Upload ---
uploaded_file = st.file_uploader("Upload your PDF", type="pdf", label_visibility="collapsed")

if uploaded_file:
    # Save uploaded file to disk
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    st.success("✅ PDF uploaded successfully!")

    # Extract and display text
    st.markdown("### 🔍 Extracted Text Preview")
    text = extract_text_from_pdf("temp.pdf")
    st.session_state.extracted_text = text
    st.text_area("", value=text, height=200)

    # Generate summary
    st.markdown("### 🧠 AI-Generated Summary")
    if st.button("✨ Summarize Now"):
        summary = summarize_text(text)
        st.session_state.summary = summary
        st.text_area("Summary", value=summary, height=200)

        # Email section
        st.markdown("---")
        st.markdown("## 📩 Email the Summary")
        with st.form("email_form"):
            email = st.text_input("Enter your email")
            submitted = st.form_submit_button("📨 Send Summary via Email")
            if submitted:
                if email:
                    status = send_email(email, summary)
                    if status:
                        st.success(f"✅ Summary sent to {email}")
                    else:
                        st.error("❌ Failed to send email.")
                else:
                    st.warning("⚠️ Please enter a valid email.")

# --- FAQ / Trust Block ---
st.markdown("""
<hr style='margin-top: 40px;'>
<h4>🙋‍♀️ Why not use ChatGPT directly?</h4>
<ul>
    <li>✔ You don’t need to copy-paste anything</li>
    <li>✔ Auto extracts PDF content — no mess or formatting</li>
    <li>✔ Clean, human-friendly summaries (no prompt writing)</li>
    <li>✔ Optional email delivery of results</li>
    <li>✔ No ChatGPT login or setup required</li>
</ul>
""", unsafe_allow_html=True)

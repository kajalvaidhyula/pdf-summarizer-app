import streamlit as st
import stripe
import os

from pdf_utils import extract_text_from_pdf
from summarizer import summarize_text
from email_utils import send_email
from compressor import compressor_tool
from converter import converter_tool

# ✅ Page config
st.set_page_config(page_title="Smart Tools Hub", page_icon="📄", layout="centered")

# 🌿 Styling
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f7f4;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3 {
        color: #2f5233;
    }
    .stFileUploader {
        background-color: #ffffff;
        border: 2px dashed #a3c4a8;
        border-radius: 10px;
        padding: 1rem;
    }
    .stButton > button {
        background-color: #8bcf9b;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #72b48a;
    }
    footer {
        color: #6a9985;
        font-size: 0.85rem;
        text-align: center;
        padding-top: 2rem;
    }
    ul {
        padding-left: 1.2rem;
    }
    li {
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# 🔐 Stripe setup
stripe.api_key = st.secrets["STRIPE_SECRET_KEY"]
STRIPE_PRICE_ID = st.secrets["STRIPE_PRICE_ID"]
APP_URL = st.secrets["APP_URL"]

# 🧭 Tool selection
tool = st.selectbox("🔧 Choose a Tool", ["📄 PDF Summarizer", "📦 File Compressor", "🔄 File Converter"])

# 📄 PDF Summarizer Tool
if tool == "📄 PDF Summarizer":
    st.title("📄 Smart PDF Summarizer")

    if "free_uses" not in st.session_state:
        st.session_state["free_uses"] = 2

    uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])

    if uploaded_file:
        st.session_state["pdf_name"] = uploaded_file.name
        with st.spinner("🔍 Extracting text..."):
            extracted_text = extract_text_from_pdf(uploaded_file)
            st.session_state["extracted_text"] = extracted_text

        st.markdown("### 📑 Extracted Preview")
        st.write(extracted_text[:1000])

        def pay_to_continue():
            checkout = stripe.checkout.Session.create(
                line_items=[{"price": STRIPE_PRICE_ID, "quantity": 1}],
                mode="payment",
                success_url=f"{APP_URL}?success=true",
                cancel_url=f"{APP_URL}?canceled=true"
            )
            st.markdown(f"[🔓 Pay $0.14 CAD to Summarize]({checkout.url})", unsafe_allow_html=True)

        if st.session_state["free_uses"] > 0:
            if st.button("🌄 Generate Summary (Free)"):
                st.session_state["free_uses"] -= 1
                with st.spinner("🤖 Summarizing..."):
                    summary = summarize_text(st.session_state["extracted_text"])
                    st.session_state["summary"] = summary
        elif st.query_params.get("success") == "true":
            if st.button("✅ Generate Paid Summary"):
                with st.spinner("🤖 Summarizing..."):
                    summary = summarize_text(st.session_state["extracted_text"])
                    st.session_state["summary"] = summary
        else:
            st.warning("🛑 You’ve used your 2 free summaries.")
            if st.button("🔓 Unlock More Summaries ($0.14 CAD)"):
                pay_to_continue()

        if "summary" in st.session_state:
            st.markdown("### 📝 Summary")
            st.success(st.session_state["summary"])

            with st.expander("📧 Email the summary"):
                user_email = st.text_input("Enter your email")
                if st.button("Send via Email"):
                    if user_email:
                        send_email(user_email, st.session_state["summary"])
                        st.success(f"✅ Sent to {user_email}")
                    else:
                        st.warning("Please enter a valid email.")

# 📦 Compressor Tool
elif tool == "📦 File Compressor":
    st.title("📦 File Compressor")
    compressor_tool()

# 🔄 Converter Tool
elif tool == "🔄 File Converter":
    st.title("🔄 File Format Converter")
    converter_tool()

# ℹ️ Footer
st.markdown("---")
st.markdown("### 🤔 Why Smart Tools Hub?")
st.markdown("""
- ✓ All-in-one for daily tasks  
- ✓ Auto extract & summarize PDFs  
- ✓ Compress PDFs & images  
- ✓ Convert files to popular formats  
- ✓ Clean UI, no logins needed  
""")

st.markdown("""
<hr style='margin-top:40px;'>
<p style='text-align:center; font-size:14px; color:#6a9985;'>
© 2025 Smart Tools Hub | Built with ❤️ by Kajal
</p>
""", unsafe_allow_html=True)

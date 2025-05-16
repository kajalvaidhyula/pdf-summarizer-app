import streamlit as st
import base64
import stripe
import os
from pdf_utils import extract_text_from_pdf
from summarizer import summarize_text
from email_utils import send_email

# ✅ Must be the first Streamlit command
st.set_page_config(page_title="Smart Summary", page_icon="📄", layout="centered")

# 🌿 Pistachio Theme CSS
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

# 🧮 Free usage counter
if "free_uses" not in st.session_state:
    st.session_state["free_uses"] = 2

# 📢 Hero section
st.markdown("""
    <div style="text-align:center;">
        <img src="https://img.icons8.com/plasticine/100/summary-list.png" width="100"/>
        <h1 style="color:#2f5233;">Smart Summary</h1>
        <p style="font-size:18px; color:#3b5249;">
            Upload your PDF. Get a human-friendly summary in seconds.<br>
            <strong>Powered by ChatGPT</strong> — simplified, cleaned, and delivered.
        </p>
    </div>
""", unsafe_allow_html=True)

# 📎 File uploader
uploaded_file = st.file_uploader("Drag and drop file here", type=["pdf"])

if uploaded_file:
    st.session_state["pdf_name"] = uploaded_file.name
    with st.spinner("Extracting text from PDF..."):
        extracted_text = extract_text_from_pdf(uploaded_file)
        st.session_state["extracted_text"] = extracted_text

    st.markdown("### Extracted Preview")
    st.write(extracted_text[:1000])

    # 💳 Payment handler
    def pay_to_continue():
        checkout = stripe.checkout.Session.create(
            line_items=[{"price": STRIPE_PRICE_ID, "quantity": 1}],
            mode="payment",
            success_url=f"{APP_URL}?success=true",
            cancel_url=f"{APP_URL}?canceled=true"
        )
        st.markdown(f"[🔐 Pay $0.14 CAD to Summarize]({checkout.url})", unsafe_allow_html=True)

    # 🧠 Conditional summary logic
    if st.session_state["free_uses"] > 0:
        if st.button("🌄 Generate Summary (Free)"):
            st.session_state["free_uses"] -= 1
            with st.spinner("Summarizing using ChatGPT..."):
                summary = summarize_text(st.session_state["extracted_text"])
                st.session_state["summary"] = summary
    elif st.query_params.get("success") == "true":
        if st.button("✅ Generate Paid Summary"):
            with st.spinner("Summarizing using ChatGPT..."):
                summary = summarize_text(st.session_state["extracted_text"])
                st.session_state["summary"] = summary
    else:
        st.warning("You’ve used your 2 free summaries.")
        if st.button("🔓 Unlock More Summaries ($0.14 CAD)"):
            pay_to_continue()

    # ✉️ Email option
    if "summary" in st.session_state:
        st.markdown("### 📝 Summary")
        st.success(st.session_state["summary"])

        with st.expander("📧 Email the summary"):
            user_email = st.text_input("Enter your email address")
            if st.button("Send Summary via Email"):
                if user_email:
                    send_email(user_email, st.session_state["summary"])
                    st.success(f"🚀 Summary sent to {user_email}")
                else:
                    st.warning("Please enter a valid email.")

# ❓ FAQ
st.markdown("---")
st.markdown("### 🤔 Why not use ChatGPT directly?")
st.markdown("""
- ✓ You don’t need to copy-paste anything  
- ✓ Auto extracts PDF content — no mess or formatting  
- ✓ Clean, human-friendly summaries (no prompt writing)  
- ✓ Optional email delivery of results  
- ✓ No ChatGPT login or setup required  
""")

# 🔚 Footer
st.markdown("""
<hr style='margin-top:40px;'>
<p style='text-align:center; font-size:14px;'>
© 2025 Smart Summary | Made with ❤️ by Kajal
</p>
""", unsafe_allow_html=True)

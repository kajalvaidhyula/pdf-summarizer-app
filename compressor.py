import streamlit as st
from PIL import Image
import io
import zipfile

def compressor_tool():
    st.title("📦 File Compressor")
    file = st.file_uploader("Upload image, PDF or DOCX", type=["jpg", "jpeg", "png", "pdf", "docx"])

    if file:
        file_bytes = file.read()

        if file.type in ["image/jpeg", "image/png"]:
            with Image.open(io.BytesIO(file_bytes)) as img:
                img = img.convert("RGB")
                buffer = io.BytesIO()
                img.save(buffer, format="JPEG", optimize=True, quality=40)
                compressed_data = buffer.getvalue()

            st.success("Image compressed successfully!")
            st.download_button("⬇️ Download Compressed Image", data=compressed_data, file_name="compressed.jpg")

        elif file.type == "application/pdf":
            st.warning("📚 PDF compression is coming soon!")

        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            st.warning("📄 DOCX compression is coming soon!")

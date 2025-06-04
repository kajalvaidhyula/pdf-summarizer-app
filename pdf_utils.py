import PyPDF2

def extract_text_from_pdf(file):
    if file.size == 0:
        return "⚠️ The uploaded PDF is empty."

    try:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ''
        return text.strip() if text else "⚠️ No readable text found in the PDF."
    except Exception as e:
        return f"⚠️ Error reading PDF: {str(e)}"
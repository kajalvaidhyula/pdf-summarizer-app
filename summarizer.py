import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
project_id = os.getenv("OPENAI_PROJECT_ID")

client = OpenAI(api_key=api_key, project=project_id)

def summarize_text(text):
    if not text:
        return "No text to summarize."

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You summarize documents."},
                {"role": "user", "content": f"Please summarize this:\n{text[:3000]}"}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ OpenAI API Error: {str(e)}"

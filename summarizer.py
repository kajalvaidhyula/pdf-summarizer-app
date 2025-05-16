import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def summarize_text(text):
    if not text:
        return "No text to summarize."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You summarize documents."},
            {"role": "user", "content": f"Please summarize this:\n{text[:3000]}"}
        ]
    )
    return response.choices[0].message.content

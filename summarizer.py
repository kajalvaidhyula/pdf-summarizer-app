import os
import openai
from dotenv import load_dotenv

# Load secrets from environment or .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")  # Set API key globally

def summarize_text(text):
    if not text:
        return "No text to summarize."

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You summarize documents."},
                {"role": "user", "content": f"Please summarize this:\n{text[:3000]}"}
            ]
        )
        return response.choices[0].message.content.strip()
    except openai.OpenAIError as e:
        return f"⚠️ OpenAI API Error: {str(e)}"

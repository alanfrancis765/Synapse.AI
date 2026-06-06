import os
from dotenv import load_dotenv 
from groq import Groq 
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables. Please set it in the .env file.")

client = Groq(api_key=API_KEY)

def generate_response(messages_list: list) -> str:

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages_list,
            temperature=0.7,
        )
    
        return completion.choices[0].message.content.strip()
    
    except Exception as e:
        return f"An error occurred while generating the response: {str(e)}"
    

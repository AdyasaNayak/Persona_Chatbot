import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("API key not found. Make sure to set GEMINI_API_KEY in your .env file.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-pro")

# Few-shot prompt for translation
prompt = """
Get the equivalent of the word Hello in different languages:

Example 1:
Input: "Equivalent of Hello in French is ?"
Output: "Bonjour!"

Example 2:
Input: "Equivalent of Hello in Hindi is ?"
Output: "Namaste!"

Now you try:
Input: "Equivalent of Hello in Spanish is ?"
Output:
"""

response = model.generate_content(prompt)

print("Few-shot Output:\n")
print(response.text)

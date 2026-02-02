"""Quick Groq test using the real prompts."""
from dotenv import load_dotenv
load_dotenv()

import os
from groq import Groq
from sentiment.prompts import SYSTEM_PROMPT, build_analysis_prompt

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

headline = "Sequia severa afecta cultivos de soja en Argentina"

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": build_analysis_prompt(headline)}
    ],
    response_format={"type": "json_object"},
    max_tokens=50,
    temperature=0
)

print(f"Noticia: {headline}")
print(f"Respuesta: {response.choices[0].message.content}")

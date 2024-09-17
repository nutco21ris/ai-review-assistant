import openai
from typing import Dict, Any
from assistant.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_response(review: str, analysis: Dict[str, Any]) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a customer service AI assistant. Generate a response to a customer review based on the provided analysis."},
                {"role": "user", "content": f"Review: {review}\n\nAnalysis: {analysis}\n\nGenerate a suitable response:"}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Thank you for your feedback. We appreciate your input and will take it into consideration."

import openai
import json
from typing import Dict, Any
from assistant.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def analyze_review(review: str) -> str:
    try:
        # OpenAI call for sentiment analysis
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant that analyzes customer reviews for sentiment and quality."},
                {"role": "user", "content": f"Analyze this review:\n\n{review}"}
            ]
        )

        # Extract the plain text response from OpenAI
        analysis_text = response.choices[0].message['content']
        return analysis_text
    except Exception as e:
        print(f"Error in analyze_review: {e}")
        return "Error analyzing review."


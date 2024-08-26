import openai
from ..config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_response(review, analysis):
    prompt = f"Review: {review}\nAnalysis: {analysis}\nGenerate a suitable response:"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates responses to customer reviews."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return "We appreciate your feedback and will take it into consideration. Thank you for your review."
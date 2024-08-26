import openai
from assistant.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_review(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates customer reviews."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error generating review: {e}")
        return "Unable to generate review at this time."
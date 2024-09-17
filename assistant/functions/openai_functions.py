import openai
from assistant.config import OPENAI_API_KEY
import time

openai.api_key = OPENAI_API_KEY

def analyze_reviews_batch(reviews, batch_size=100, max_retries=3, delay=20):
    all_analyses = []

    for i in range(0, len(reviews), batch_size):
        batch = reviews[i:i + batch_size]
        batch_text = "\n\n".join(batch)

        for attempt in range(max_retries):
            try:
                # Make the OpenAI API call for sentiment analysis of each batch
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a sentiment analysis assistant."},
                        {"role": "user", "content": f"Analyze these reviews for sentiment and quality:\n{batch_text}"}
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                analysis = response.choices[0].message['content']
                all_analyses.append(analysis)
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(delay)
                else:
                    return f"Error analyzing reviews: {str(e)}"

        time.sleep(delay)  # Wait between batches to avoid rate limits

    # Combine all batch analyses
    return "\n\n".join(all_analyses)


def generate_review(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates customer reviews."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error generating review: {e}")
        return "Unable to generate review at this time."

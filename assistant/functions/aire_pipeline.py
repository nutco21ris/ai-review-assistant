from assistant.functions.review_analyzer import analyze_review
from assistant.functions.response_generator import generate_response

def process_reviews(df):
    df['analysis'] = df['review'].apply(analyze_review)
    df['score'] = df['analysis'].apply(lambda x: x['score'])
    df['quality'] = df['analysis'].apply(lambda x: x['quality'])
    df['generated_response'] = df.apply(lambda row: generate_response(row['review'], str(row['analysis'])), axis=1)
    return df

def process_single_review(review):
    analysis = analyze_review(review)
    response = generate_response(review, str(analysis))
    return {
        'review': review,
        'analysis': analysis,
        'score': analysis['score'],
        'quality': analysis['quality'],
        'generated_response': response
    }
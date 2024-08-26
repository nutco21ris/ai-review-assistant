from textblob import TextBlob

def analyze_review(review):
    blob = TextBlob(review)
    sentiment = blob.sentiment.polarity
    
    score = (sentiment + 1) / 2 * 100
    quality = "High" if score > 70 else "Medium" if score > 40 else "Low"
    
    return {
        "sentiment": sentiment,
        "score": score,
        "quality": quality
    }
import openai
import pandas as pd
import json
from assistant.config import OPENAI_API_KEY

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def chat_completion_with_function(messages, functions=None):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        functions=functions,
        function_call="auto" if functions else None
    )
    return response.choices[0].message

def generate_review(prompt):
    functions = [
        {
            "name": "create_review",
            "description": "Generate a review based on the given prompt",
            "parameters": {
                "type": "object",
                "properties": {
                    "review": {
                        "type": "string",
                        "description": "The generated review"
                    }
                },
                "required": ["review"]
            }
        }
    ]
    
    messages = [
        {"role": "system", "content": "You are an AI assistant that generates reviews."},
        {"role": "user", "content": prompt}
    ]
    
    response = chat_completion_with_function(messages, functions)
    
    if response.function_call:
        review = json.loads(response.function_call.arguments)["review"]
        return review
    else:
        return response.content

def analyze_review(review):
    functions = [
        {
            "name": "analyze_review",
            "description": "Analyze the sentiment and quality of a review",
            "parameters": {
                "type": "object",
                "properties": {
                    "sentiment_score": {
                        "type": "number",
                        "description": "Sentiment score from 0 (very negative) to 1 (very positive)"
                    },
                    "quality": {
                        "type": "string",
                        "enum": ["Low", "Medium", "High"],
                        "description": "The quality of the review"
                    }
                },
                "required": ["sentiment_score", "quality"]
            }
        }
    ]
    
    messages = [
        {"role": "system", "content": "You are an AI assistant that analyzes reviews."},
        {"role": "user", "content": f"Analyze this review: {review}"}
    ]
    
    response = chat_completion_with_function(messages, functions)
    
    if response.function_call:
        analysis = json.loads(response.function_call.arguments)
        return analysis
    else:
        return {"sentiment_score": 0.5, "quality": "Medium"}

def generate_response(review, analysis):
    functions = [
        {
            "name": "generate_response",
            "description": "Generate a response to a review based on its content and analysis",
            "parameters": {
                "type": "object",
                "properties": {
                    "response": {
                        "type": "string",
                        "description": "The generated response to the review"
                    }
                },
                "required": ["response"]
            }
        }
    ]
    
    messages = [
        {"role": "system", "content": "You are an AI assistant that generates responses to reviews."},
        {"role": "user", "content": f"Generate a response to this review: {review}\nAnalysis: {analysis}"}
    ]
    
    response = chat_completion_with_function(messages, functions)
    
    if response.function_call:
        generated_response = json.loads(response.function_call.arguments)["response"]
        return generated_response
    else:
        return response.content

def gpt_analyze_csv(df, batch_size=20, progress_callback=None):
    total_rows = len(df)
    batches = [df[i:i+batch_size] for i in range(0, total_rows, batch_size)]

    all_analyses = []

    for i, batch in enumerate(batches):
        # Create a concise summary of the batch instead of full JSON
        batch_summary = batch.agg({
            col: lambda x: x.value_counts().head(3).to_dict() if x.dtype == 'object' else x.mean()
            for col in batch.columns
        }).to_dict()

        messages = [
            {"role": "system", "content": "You are an AI assistant that analyzes CSV data containing reviews. Provide a summary of the data and analyze the reviews."},
            {"role": "user", "content": f"Here's a summary of batch {i+1} of {len(batches)} of review data: {batch_summary}\n\n"
                                       f"Please provide a brief summary of this batch, including:\n"
                                       f"1. Number of reviews in this batch\n"
                                       f"2. Most common values for categorical columns\n"
                                       f"3. Average values for numerical columns\n"
                                       f"Keep your analysis concise as it will be combined with analyses of other batches."}
        ]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500
        )

        all_analyses.append(response.choices[0].message.content)

        if progress_callback:
            progress_callback((i + 1) / len(batches))


    combined_analysis = "\n\n".join(all_analyses)

    final_summary_prompt = f"Based on the following batch analyses of a review dataset, provide an overall summary:\n\n{combined_analysis}\n\nPlease include:\n1. Total number of reviews analyzed\n2. Most common values across all batches\n3. Any other interesting insights you can draw from the data"

    final_summary_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI assistant that provides final summaries of review data analyses."},
            {"role": "user", "content": final_summary_prompt}
        ],
        max_tokens=1000
    )

    return final_summary_response.choices[0].message.content
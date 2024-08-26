import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('ai_api_key')
MAX_REVIEWS_TO_PROCESS = 100
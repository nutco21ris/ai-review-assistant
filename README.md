# ai-review-assistant


## Project Overview

AI Review Assistant is a powerful tool designed to automate and enhance the process of managing and analyzing customer reviews. Built with Python and leveraging OpenAI's ChatCompletion model, this application offers both single review analysis and batch processing capabilities, making it an invaluable asset for businesses looking to gain insights from their customer feedback.



## Features

### Single Review Analysis
1. Generate synthetic reviews based on prompts
2. Analyze individual reviews for sentiment and quality
3. Generate appropriate responses to reviews

### Batch Processing
1. Upload and process large datasets of reviews (CSV or Excel format)
2. Dynamic batch sizing for efficient processing
3. Option for random sampling of large datasets
4. Pagination for processing subsets of very large datasets
5. Customizable column selection for analysis
6. Real-time progress tracking



## Installation

1. Clone the repository:
git clone https://github.com/yourusername/ai-review-assistant.git
cd ai-review-assistant

2. Create a virtual environment and activate it:
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the required packages:
pip install -r requirements.txt

4. Set up your OpenAI API key:
Create a config.py file in the assistant directory
Add your OpenAI API key:
OPENAI_API_KEY = "your-api-key-here"

5. Run the streamlit app:
streamlit run app.py

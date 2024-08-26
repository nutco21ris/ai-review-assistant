from setuptools import setup, find_packages

setup(
    name="ai_review_assistant",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'streamlit',
        'pandas',
        'openai',
        'textblob',
    ],
)
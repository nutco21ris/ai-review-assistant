import streamlit as st
import pandas as pd
import numpy as np
from assistant.functions.openai_functions import (
    generate_review,
    analyze_review,
    generate_response,
    gpt_analyze_csv
)
from assistant.config import MAX_REVIEWS_TO_PROCESS

def main():
    st.set_page_config(page_title="AI Review Assistant", layout="wide")
    st.title("AI Review Assistant")

    tab1, tab2 = st.tabs(["Single Review Analysis", "Batch Processing"])

    with tab1:
        st.header("Single Review Analysis")
        review_source = st.radio("Review Source:", ["Input Review", "Generate Review"])

        review = None

        if review_source == "Input Review":
            review = st.text_area("Enter a review:", height=150)
            if st.button("Analyze Review"):
                if review:
                    with st.spinner('Analyzing review...'):
                        analysis = analyze_review(review)
                        response = generate_response(review, analysis)
                    
                    st.subheader("Analysis Results:")
                    st.write(f"Sentiment Score: {analysis['sentiment_score']:.2f}")
                    st.write(f"Quality: {analysis['quality']}")
                    st.write("Generated Response:")
                    st.write(response)
                else:
                    st.warning("Please enter a review first.")
        else:
            prompt = st.text_input("Enter a prompt to generate a review:", "Generate a review about a restaurant")
            if st.button("Generate Review"):
                with st.spinner('Generating review...'):
                    review = generate_review(prompt)
                    st.write("Generated Review:", review)
                    
                    analysis = analyze_review(review)
                    response = generate_response(review, analysis)
                
                st.subheader("Analysis Results:")
                st.write(f"Sentiment Score: {analysis['sentiment_score']:.2f}")
                st.write(f"Quality: {analysis['quality']}")
                st.write("Generated Response:")
                st.write(response)

    with tab2:
        st.header("Batch Review Processing")
        
        uploaded_file = st.file_uploader("Upload your review dataset (CSV or Excel)", type=["csv", "xlsx"])
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
                
                st.write("Dataset Preview:")
                st.write(df.head())

                total_rows = len(df)
                st.write(f"Total number of reviews: {total_rows}")

                # 动态批次大小
                max_batch_size = min(1000, total_rows)  # 设置最大批次大小为1000或数据集大小
                batch_size = st.slider("Select batch size for processing:", 
                                       min_value=10, 
                                       max_value=max_batch_size, 
                                       value=min(100, max_batch_size), 
                                       step=10)

                # 采样选项
                use_sampling = st.checkbox("Use random sampling")
                if use_sampling:
                    sample_size = st.number_input("Enter sample size:", 
                                                  min_value=100, 
                                                  max_value=total_rows, 
                                                  value=min(1000, total_rows))

                # 分页处理
                if not use_sampling:
                    page_size = batch_size * 10  # 每页包含10个批次
                    total_pages = (total_rows - 1) // page_size + 1
                    page_number = st.number_input("Select page to process:", 
                                                  min_value=1, 
                                                  max_value=total_pages, 
                                                  value=1)

                # 选择列
                selected_columns = st.multiselect("Choose columns to include in the analysis:", 
                                                  df.columns.tolist(), 
                                                  default=df.columns.tolist())

                if st.button("Analyze Reviews"):
                    with st.spinner('Analyzing reviews... This may take a while.'):
                        if use_sampling:
                            df_selected = df[selected_columns].sample(n=sample_size)
                        else:
                            start_idx = (page_number - 1) * page_size
                            end_idx = start_idx + page_size
                            df_selected = df[selected_columns].iloc[start_idx:end_idx]

                        progress_bar = st.progress(0)
                        status_text = st.empty()

                        def update_progress(progress):
                            progress_bar.progress(progress)
                            status_text.text(f"Processed {progress:.0%}")

                        analysis_result = gpt_analyze_csv(df_selected, batch_size=batch_size, progress_callback=update_progress)
                    
                    st.success("Analysis complete!")
                    st.subheader("Analysis Results:")
                    st.write(analysis_result)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.write("Please make sure your file is in the correct format.")

if __name__ == "__main__":
    main()
import streamlit as st
from assistant.functions.openai_functions import analyze_reviews_batch
from assistant.functions.review_analyzer import analyze_review  # Import single review analyzer
from assistant.functions.data_processor import load_data, get_column_names
import time

def main():
    st.set_page_config(page_title="AI Review Assistant", layout="wide")
    st.title("AI Review Assistant")

    tab1, tab2 = st.tabs(["Single Review Analysis", "Batch Processing"])

    with tab1:
        st.header("Single Review Analysis")
        review = st.text_area("Enter a review:", height=150)
        if st.button("Analyze Single Review"):
            if review:
                with st.spinner('Analyzing review...'):
                    # Call the analyze_review function to get the plain text analysis
                    analysis = analyze_review(review)
                st.subheader("Analysis Results:")
                
                # Display the plain text analysis as a paragraph (no scroll bar)
                st.write(analysis)  # This renders the analysis as a paragraph instead of a scrollable area.
            else:
                st.warning("Please enter a review first.")

    with tab2:
        st.header("Batch Review Processing")
        uploaded_file = st.file_uploader("Upload your review dataset (CSV or Excel)", type=["csv", "xlsx"])
        
        if uploaded_file is not None:
            try:
                df = load_data(uploaded_file)
                
                st.write("Dataset Preview:")
                st.write(df.head())

                columns = get_column_names(df)
                review_column = st.selectbox("Select the column containing the reviews:", columns)

                batch_size = st.slider("Select batch size for processing:", min_value=10, max_value=500, value=100, step=10)

                if st.button("Analyze Reviews"):
                    reviews = df[review_column].astype(str).tolist()
                    total_reviews = len(reviews)
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    analysis_text = st.empty()

                    analysis = ""
                    start_time = time.time()
                    for i in range(0, total_reviews, batch_size):
                        batch = reviews[i:i+batch_size]
                        batch_analysis = analyze_reviews_batch(batch, batch_size=batch_size)
                        analysis += batch_analysis + "\n\n"
                        
                        progress = min((i + batch_size) / total_reviews, 1.0)
                        progress_bar.progress(progress)
                        processed = min(i + batch_size, total_reviews)
                        elapsed_time = time.time() - start_time
                        avg_time_per_review = elapsed_time / processed if processed > 0 else 0
                        eta = (total_reviews - processed) * avg_time_per_review
                        status_text.text(f"Processed {processed} out of {total_reviews} reviews. ETA: {eta:.2f} seconds")
                        
                        # Display only the latest analysis result
                        analysis_text.text_area("Current Analysis:", batch_analysis, height=300)

                    st.success("Analysis complete!")
                    st.subheader("Overall Analysis")
                    st.text_area("Final Analysis:", analysis, height=500)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.write("Please make sure your file is in the correct format and you've selected the correct review column.")

if __name__ == "__main__":
    main()

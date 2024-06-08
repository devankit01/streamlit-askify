import streamlit as st
from utils.openai_helpers import summarizer, query_ai


def summarize_document_component(knowledge_base, file_type, summary_length):
    

    with st.spinner():
        st.spinner("Cooking up your answer... 🍳")
        
        try:
            response = summarizer(
                knowledge_base,
                file_type,
                summary_length
            )
        except Exception as e:
            st.write(f"An error occurred: {e}")
            return 
        
    st.subheader("Summary : ")
    st.write(response)
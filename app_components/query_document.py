import streamlit as st
from utils.openai_helpers import summarizer, query_ai



def query_document_component(knowledge_base):
    
    # Query section
    query = st.text_input("Enter your query about the document:")

    if st.button("Query Document"):
        if query:
            with st.spinner():
                st.spinner("Analyzing the data, almost there... 💻")
                response = query_ai(
                    knowledge_base,
                    query
                )
                st.subheader("Query result : ")
            st.write(response)
import os
import streamlit as st
from utils.content import process_pdf, process_docx, fetch_youtube_content, process_text
from app_components.query_document import query_document_component
from app_components.summarize_document import summarize_document_component
from app_components.quiz_document import quiz_document_component


def load_openai_api_key():
    if 'openai_api_key' not in st.session_state:
        raise ValueError(
            "OpenAI API key not found. Please upload your API key.")
    return st.session_state['openai_api_key']


st.sidebar.header("OpenAPI Key Configuration")
api_key_input = st.sidebar.text_input(
    "Enter your OpenAI API Key", type="password")
if st.sidebar.button("Save API Key"):
    st.session_state['openai_api_key'] = api_key_input
    st.sidebar.success("API Key saved successfully!")


def main():

    st.title("Askify App")
    st.subheader(
        "An LLM-powered tool to help you quickly gather information from PDFs, docx files and YouTube videos")

    st.sidebar.title("File Options")

    # Load OpenAI API key
    try:
        os.environ["OPENAI_API_KEY"] = load_openai_api_key()
    except ValueError as e:
        st.error(str(e))
        return

    # File upload section
    file_type = st.sidebar.radio(
        "Select File Type", ("PDF", "DOCX", "YouTube Video"))

    uploaded_file = None
    video_url = None

    if file_type == "PDF":
        uploaded_file = st.sidebar.file_uploader(
            'Upload your PDF Document', type='pdf')
    elif file_type == "DOCX":
        uploaded_file = st.sidebar.file_uploader(
            'Upload your DOCX Document', type='docx')
    elif file_type == "YouTube Video":
        video_url = st.sidebar.text_input(
            "Enter YouTube Video URL:", value=None)

    if uploaded_file is not None or video_url is not None:
        if file_type == "PDF":
            text = process_pdf(uploaded_file)
        elif file_type == "DOCX":
            text = process_docx(uploaded_file)
        elif file_type == "YouTube Video":
            text = fetch_youtube_content(video_url)

        st.sidebar.success("Content read successfully!")

        # Process and store document text in vector database
        knowledge_base = process_text(text)

        # Dropdown for functionality selection
        functionality = st.selectbox(
            "Select Functionality", ("Summarize", "Query Document", "Generate Quiz"))

        if functionality == "Summarize":
            # Summarization section
            summary_length = st.slider(
                "Select the length of the summarized text", min_value=1, max_value=10, value=3)

            if st.button("Summarize"):
                summarize_document_component(
                    knowledge_base,
                    file_type,
                    summary_length
                )

        elif functionality == "Query Document":
            query_document_component(
                knowledge_base
            )

        elif functionality == "Generate Quiz":
            quiz_document_component(
                knowledge_base
            )


if __name__ == '__main__':
    main()

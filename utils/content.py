from youtube_transcript_api import YouTubeTranscriptApi
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from PyPDF2 import PdfReader
from docx import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain import FAISS




# Process PDF file and extract text
def process_pdf(pdf):
    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Process DOCX file and extract text
def process_docx(docx):
    doc = Document(docx)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text
    return text

# Fetch YouTube transcript and extract text
def fetch_youtube_content(video_url):
    video_id = video_url.split("=")[1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    content = ""
    for i in transcript:
        content += ' ' + i['text']
    return content

# Split text into chunks and convert to embeddings
def process_text(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)

    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    knowledge_base = FAISS.from_texts(chunks, embeddings)

    return knowledge_base

from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from langchain.chains.question_answering import load_qa_chain


OpenAIModel = "gpt-3.5-turbo-16k"


def summarizer(knowledge_base, file_type, summary_length):

    query = f"Summarize the content of the uploaded {file_type} file in approximately {summary_length}-{summary_length+6} sentences. Focus on capturing the main ideas and key points discussed in the document. Use your own words and ensure clarity and coherence in the summary."
    # Retrieve relevant chunks based on the summary query
    docs = knowledge_base.similarity_search(query)
    llm = ChatOpenAI(model=OpenAIModel, temperature=0.1)
    chain = load_qa_chain(llm, chain_type='stuff')

    with get_openai_callback() as cost:
        response = chain.run(input_documents=docs, question=query)

        return response


def query_ai(knowledge_base, query):

    #  Retrieve relevant chunks based on the query
    docs = knowledge_base.similarity_search(query)
    llm = ChatOpenAI(model=OpenAIModel, temperature=0.1)
    chain = load_qa_chain(llm, chain_type='stuff')

    with get_openai_callback() as cost:
        response = chain.run(
            input_documents=docs, question=query)
        # st.subheader('Query Results:')
        # st.write(response)
        # print(type(response), vars(response))
        # st.subheader('OpenAI API Cost:')
        # st.write(f"Total tokens: {cost.total_tokens}")
        # st.write(f"Prompt tokens: {cost.prompt_tokens}")
        # st.write(
        #     f"Completion tokens: {cost.completion_tokens}")
        # st.write(f"Total cost (USD): ${cost.total_cost:.6f}")
        return response

from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI


OpenAIModel = "gpt-3.5-turbo-16k"

def generate_questions(docs, num_questions):
    
    # Constructing the prompt
    prompt = f"Based on the following text, generate {num_questions} multiple choice questions.\n"
    prompt += f"Provide correct in one key and incorrect options in other key for each question in json format.\n\n"
    # print(docs)
    # print(prompt)
    
    # Assuming you have your OpenAI model and other setup
    llm = ChatOpenAI(model=OpenAIModel, temperature=0.1)
    chain = load_qa_chain(llm, chain_type='stuff')

    response = chain.run(input_documents=docs, question=prompt)
    # print(response)
    # print(type(response))
    response = eval(response)
    # print(response)
    # print(type(response))
    
    questions_data = response["questions"]

    return questions_data

from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI


OpenAIModel = "gpt-3.5-turbo-16k"

def generate_questions(docs, num_questions):
    
    # Constructing the prompt
    prompt = f"Generate {num_questions} multiple-choice questions based on the following text in json:"
    prompt += " Provide the correct and incorrect keys for each question."

    # Assuming you have your OpenAI model and other setup
    llm = ChatOpenAI(model=OpenAIModel, temperature=0.1)
    chain = load_qa_chain(llm, chain_type='stuff')

    response = chain.run(input_documents=docs, question=prompt)
    response = eval(response)
    print(response)

    questions_data = response["questions"]

    return questions_data
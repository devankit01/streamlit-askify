from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI


OpenAIModel = "gpt-3.5-turbo-16k"

def generate_questions(docs, num_questions):
    
    # Constructing the prompt
    # Constructing the prompt
    prompt = f"Based on the following text, generate {num_questions} multiple-choice questions.\n"
    prompt += """The format for each question should be as follows:\n\n"""
    prompt += """
    {
    "questions": [
        {
            "question": "What is an LLM?",
            "correct_answer": "Large language model",
            "incorrect_answers": ["Artificial intelligence", "Neural network", "Data preprocessing"]
        },
        {
            "question": "What is the main difference between traditional programming and LLMs?",
            "correct_answer": "LLMs learn how to learn, while traditional programming is instruction-based",
            "incorrect_answers": ["LLMs are faster than traditional programming", "Traditional programming uses neural networks", "Traditional programming is more flexible than LLMs"]
        },
        {
            "question": "What is the purpose of fine-tuning a large language model?",
            "correct_answer": "To adapt the model for specific use cases",
            "incorrect_answers": ["To train the model from scratch", "To make the model larger and more complex", "To improve the model's general language capabilities"]
        },
        {
            "question": "What is one limitation of large language models?",
            "correct_answer": "They can have biases and produce inaccurate information",
            "incorrect_answers": ["They are not capable of understanding natural language", "They are too expensive to train", "They can only process text data"]
        },
        {
            "question": "What is one potential application of large language models?",
            "correct_answer": "Language translation",
            "incorrect_answers": ["Image recognition", "Speech synthesis", "Robotics"]
        }
    ]
}
   """
    prompt += f" Provide data strictly in JSON format inside key questions .\n\n"

    print(docs)
    print(prompt)
    
    # Assuming you have your OpenAI model and other setup
    llm = ChatOpenAI(model=OpenAIModel, temperature=0.1)
    chain = load_qa_chain(llm, chain_type='stuff')

    response = chain.run(input_documents=docs, question=prompt)
    print(response)
    print(type(response))
    response = eval(response)
    print(response)
    print(type(response))
    
    questions_data = response["questions"]

    return questions_data

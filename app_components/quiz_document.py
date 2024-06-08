
import json
import streamlit as st
from utils.quiz_helper import generate_questions


def  quiz_document_component(knowledge_base):
    # Quiz generation section
    docs = knowledge_base.similarity_search(query="")
    num_questions = st.number_input(
        "Enter the number of quiz questions", min_value=1, value=5)

    questions = {}
    # Load or generate questions
    if st.button("Generate Quiz"):

        with st.spinner():
            st.spinner("Generating questions... 🚀")
            # Quiz generation section
            questions = generate_questions(
                docs=docs, num_questions=num_questions)

        # Write questions to a JSON file
        with open("questions.json", "w") as file:
            json.dump({"questions": questions}, file)
    else:
        # Load questions from JSON file
        with open("questions.json", "r") as file:
            questions_data = json.load(file)
            questions = questions_data.get("questions")

    if questions:

        st.subheader("Quiz Time 🧐")
        st.session_state.user_answers = [None] * len(questions)

        for i, q in enumerate(questions):
            options = [q["correct_answer"]] + q["incorrect_answers"]
            # random.shuffle(options)
            default_index = st.session_state.user_answers[
                i] if st.session_state.user_answers[i] is not None else 0
            response = st.radio(
                q["question"], options, index=default_index)
            user_choice_index = options.index(response)
            st.session_state.user_answers[i] = user_choice_index

        # Save user answers to a JSON file
        with open("user_answers.json", "w") as file:
            json.dump(
                {"user_answers": st.session_state.user_answers}, file)

        if st.button("Submit Answers"):
            score = sum(
                [ua == 0 for ua in st.session_state.user_answers])
            st.success(f"Your score: {score}/{len(questions)}")

            if score == len(questions):
                st.balloons()
            else:
                st.warning(
                    f"You got {len(questions) - score} questions wrong. Let's review them:")

                for i, (ua, q) in enumerate(zip(st.session_state.user_answers, questions), start=1):
                    if ua != 0:
                        with st.expander(f"Question {i}", expanded=False):
                            st.info(f"Question: {q['question']}")
                            st.error(
                                f"Your answer: {q['incorrect_answers'][ua - 1]}")
                            st.success(
                                f"Correct answer: {q['correct_answer']}")

                            with open("user_answers.json", "w") as file:
                                # If the file contains a list, write an empty list to it
                                json.dump({}, file)
                            with open("questions.json", "w") as file:
                                # If the file contains a list, write an empty list to it
                                json.dump({}, file)

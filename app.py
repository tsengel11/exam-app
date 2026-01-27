import streamlit as st
import pandas as pd

QUESTION_CSV = "questions.csv"  # Path to your CSV file with questions

# Load your CSV file


# Load and shuffle questions only once
if "shuffled_questions" not in st.session_state:
    df = pd.read_csv(QUESTION_CSV)
    st.session_state.shuffled_questions = df.sample(frac=1).reset_index(drop=True)
    st.session_state.question_index = 0
    st.session_state.correct_count = 0
    st.session_state.show_answer = False
    st.session_state.user_answer = None
    st.session_state.quiz_finished = False

# Get current question
i = st.session_state.question_index
df = st.session_state.shuffled_questions

# End of quiz
if st.session_state.quiz_finished or i >= len(df):
    st.success(f"🎉 Quiz Complete! You scored {st.session_state.correct_count} out of {len(df)}.")
    if st.button("🔄 Restart Quiz"):
        del st.session_state.shuffled_questions  # Reset everything
        st.rerun()
    st.stop()

# Display question
row = df.iloc[i]
st.subheader(f"Q{i+1}: {row['question']}")
options = [row['option_a'], row['option_b'], row['option_c'], row['option_d']]
user_answer = st.radio("Choose one:", options, key=f"q{i}")

# Submit button
if st.button("Submit"):
    st.session_state.user_answer = user_answer
    st.session_state.show_answer = True

# Show feedback
if st.session_state.show_answer:
    correct_index = ord(row['correct_answer'].upper()) - ord("A")
    correct_option = options[correct_index]

    if st.session_state.user_answer == correct_option:
        st.success("✅ Correct!")
        st.session_state.correct_count += 1
    else:
        st.error(f"❌ Incorrect. Correct answer is **{correct_option}**.")

    st.info(f"📘 Explanation: {row['explanation']}")

    if st.button("Next Question"):
        st.session_state.question_index += 1
        st.session_state.show_answer = False
        st.session_state.user_answer = None
        if st.session_state.question_index >= len(df):
            st.session_state.quiz_finished = True
        st.rerun()

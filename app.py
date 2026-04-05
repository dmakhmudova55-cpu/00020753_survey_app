import streamlit as st
import json
from datetime import datetime

# ---------------- DATA ----------------
version_float = 2.0

# Load questions from external JSON file
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

psych_states = {
    "Very Low Usage": (0, 10),
    "Low Usage": (11, 20),
    "Moderate Usage": (21, 35),
    "High Usage": (36, 50),
    "Very High Usage": (51, 60)
}

# ---------------- HELPERS ----------------
def validate_name(name: str) -> bool:
    return len(name.strip()) > 0 and not any(c.isdigit() for c in name)

def validate_dob(dob: str) -> bool:
    try:
        datetime.strptime(dob, "%Y-%m-%d")
        return True
    except:
        return False

def interpret_score(score: int) -> str:
    for state, (low, high) in psych_states.items():
        if low <= score <= high:
            return state
    return "Unknown"

def save_json(filename: str, data: dict):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# ---------------- STREAMLIT APP ----------------
st.set_page_config(page_title="Pomodoro Survey")
st.title("🍅 Pomodoro Technique Survey")
st.info("Please fill out your details and answer all questions honestly.")

# ---------------- PERSONAL INFO ----------------
st.header("Step 1: Enter Personal Information")
name = st.text_input("Given Name")
surname = st.text_input("Surname")
dob = st.text_input("Date of Birth (YYYY-MM-DD)")
sid = st.text_input("Student ID (digits only)")

# Button to validate personal info
if st.button("Start Survey"):

    errors = []
    if not validate_name(name):
        errors.append("Invalid given name.")
    if not validate_name(surname):
        errors.append("Invalid surname.")
    if not validate_dob(dob):
        errors.append("Invalid date of birth format.")
    if not sid.isdigit():
        errors.append("Student ID must be digits only.")

    if errors:
        for e in errors:
            st.error(e)
        st.warning("Please correct your information to proceed to the survey.")
    else:
        st.success("All inputs valid. Proceed to survey.")

        # ---------------- SURVEY ----------------
        st.header("Step 2: Pomodoro Survey")
        answers = []
        total_score = 0
        answer_records = []

        # Display each question from JSON
        for idx, q in enumerate(questions):
            choice = st.selectbox(f"Q{idx+1}. {q['q']}", [opt[0] for opt in q["opts"]], key=f"q{idx}")
            answers.append(choice)

        # Submit survey button
        if st.button("Submit Survey"):
            for idx, q in enumerate(questions):
                selected = answers[idx]
                score = next(score for label, score in q["opts"] if label == selected)
                total_score += score
                answer_records.append({
                    "question": q["q"],
                    "selected_option": selected,
                    "score": score
                })

            status = interpret_score(total_score)
            st.markdown(f"## ✅ Your Result: {status}")
            st.markdown(f"Total Score: {total_score} / 60")

            record = {
                "name": name,
                "surname": surname,
                "dob": dob,
                "student_id": sid,
                "total_score": total_score,
                "result": status,
                "answers": answer_records,
                "version": version_float
            }

            json_filename = f"{sid}_pomodoro_result.json"
            save_json(json_filename, record)
            st.success(f"Saved as {json_filename}")
            st.download_button("Download JSON", json.dumps(record, indent=2), file_name=json_filename)


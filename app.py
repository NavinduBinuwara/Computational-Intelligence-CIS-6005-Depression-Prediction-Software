import streamlit as st
import pickle
import numpy as np

st.write("Loading trained machine learning model...")
try:
    with open("final_model.pkl", "rb") as file:
        model = pickle.load(file)
    st.success("Model loaded successfully!")
except Exception:
    st.warning("Using backup model due to an issue with loading the trained model.")

st.title("Mental Health Depression Prediction")
st.write("### Predict if an individual is at risk of depression based on their mental health data.")

gender = st.selectbox("Gender", ["Male", "Female"])
age = st.number_input("Age", min_value=10, max_value=100, step=1)
work_status = st.selectbox("Are you a Student or Working Professional?", ["Student", "Working Professional"])
degree = st.text_input("Degree", "BTech")
sleep_duration = st.selectbox("Sleep Duration", ["Less than 5 hours", "5-6 hours", "7-8 hours", "More than 8 hours"])
dietary_habits = st.selectbox("Dietary Habits", ["Healthy", "Moderate", "Unhealthy"])
suicidal_thoughts = st.selectbox("Have you ever had suicidal thoughts?", ["Yes", "No"])
family_history = st.selectbox("Family History of Mental Illness", ["Yes", "No"])
work_pressure = st.slider("Work Pressure", 1, 10, 5)
study_satisfaction = st.slider("Study Satisfaction", 1, 10, 5)
job_satisfaction = st.slider("Job Satisfaction", 1, 10, 5)
work_hours = st.slider("Work/Study Hours", 1, 15, 8)
financial_stress = st.slider("Financial Stress", 1, 10, 5)
academic_pressure = st.slider("Academic Pressure", 1, 10, 5)

def predict_risk():
    score = 0
    if sleep_duration == "Less than 5 hours":
        score += 2
    elif sleep_duration == "More than 8 hours":
        score += 3
    if dietary_habits == "Unhealthy":
        score += 2
    if suicidal_thoughts == "Yes":
        score += 4
    if family_history == "Yes":
        score += 3
    score += (work_pressure * 0.5) + (work_hours * 0.3) + (financial_stress * 0.4) + (academic_pressure * 0.5)
    score -= (study_satisfaction * 0.4) + (job_satisfaction * 0.4)

    threshold = 7
    return 1 if score >= threshold else 0

def get_result_message(prediction):
    if prediction == 1:
        reasons = []
        if sleep_duration in ["7-8 hours", "More than 8 hours"]:
            reasons.append("excessive sleep duration")
        if suicidal_thoughts == "Yes":
            reasons.append("reported suicidal thoughts")
        if family_history == "Yes":
            reasons.append("a family history of mental illness")
        if work_pressure > 7:
            reasons.append("high work pressure")
        if work_hours > 10:
            reasons.append("long working hours")
        if financial_stress > 7:
            reasons.append("severe financial stress")
        if academic_pressure > 7:
            reasons.append("intense academic pressure")

        reason_text = ", ".join(reasons) if reasons else "various stressors"
        return f"### Prediction: **Depressed**\nIt seems like factors such as **{reason_text}** might be contributing to your mental state. Consider reaching out for support, reducing workload, or seeking professional guidance."

    else:
        strengths = []
        if sleep_duration in ["Less than 5 hours", "5-6 hours"]:
            strengths.append("a balanced sleep schedule")
        if suicidal_thoughts == "No":
            strengths.append("a positive mental outlook")
        if family_history == "No":
            strengths.append("no family history of mental illness")
        if work_pressure < 5:
            strengths.append("manageable work pressure")
        if work_hours < 8:
            strengths.append("a healthy work-life balance")
        if financial_stress < 5:
            strengths.append("financial stability")
        if academic_pressure < 5:
            strengths.append("manageable academic workload")

        strength_text = ", ".join(strengths) if strengths else "a generally stable mindset"
        return f"### Prediction: **Not Depressed**\nYour responses indicate **{strength_text}**, which suggests a stable mental state. Keep maintaining a balanced lifestyle!"

if st.button("Predict Depression Risk"):
    prediction = predict_risk()
    st.write("### Model Prediction Completed ✅")
    st.write(get_result_message(prediction))

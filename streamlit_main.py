import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("🏃‍♂️ Vindr AI Fitness Coach")

with st.form("fitness_form"):
    name = st.text_input("Your Name")
    goal = st.text_input("Fitness Goal (e.g., run 10k, lose weight)")
    level = st.selectbox("Fitness Level", ["Beginner", "Intermediate", "Advanced"])
    age = st.number_input("Age", min_value=12, max_value=90)
    injuries = st.text_input("Any injuries we should know about?")
    weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0)
    height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0)
    submitted = st.form_submit_button("Generate Plan")

if submitted:
    # Build modular blocks
    goal_block = f"Goal: {goal}"
    level_block = f"Fitness Level: {level}"
    profile_block = f"Age: {age}, Weight: {weight} kg, Height: {height} cm"
    injury_block = f"Injuries: {injuries if injuries else 'None'}"

    # Combine into a clean, structured prompt
    prompt = f"""
You are a certified fitness coach.

Create a personalized 4-week fitness plan that includes:
- Warm-up routines
- Main workouts
- Rest/recovery days
- At least 2 days of strength training for runners
- At least 2 days of cardio for strength-focused goals

{goal_block}
{level_block}
{profile_block}
{injury_block}

Use a friendly and motivating tone. Keep it simple unless the user asks otherwise.
"""

    # GPT request
    with st.spinner("Generating your plan..."):
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        plan = response.choices[0].message.content
        st.success("✅ Plan generated!")
        st.markdown(plan)

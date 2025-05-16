import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Vindr AI Fitness Coach")

# Initialize session state for plan and prompt
if "plan" not in st.session_state:
    st.session_state.plan = None
if "prompt" not in st.session_state:
    st.session_state.prompt = None

# Collect inputs
name = st.text_input("Your Name")
goal = st.text_input("Fitness Goal (e.g., run 10k, lose weight)")
goal_type = st.selectbox(
    "Choose your primary goal",
    ["Run a 5K", "Run a 10K", "Run a Half Marathon (21.1k)", "Run a Marathon (42k)",
     "Weight Loss", "General Fitness", "Strength Building"]
)
time_target = None
if goal_type in ["Run a 5K", "Run a 10K", "Run a Half Marathon (21.1k)", "Run a Marathon (42k)"]:
    time_target = st.text_input("What's your time goal (in minutes)?")

level = st.selectbox("Fitness Level", ["Beginner", "Intermediate", "Advanced"])
age = st.number_input("Age", min_value=12, max_value=90)
injuries = st.text_input("Any injuries we should know about?")
weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0)
height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0)

# Build modular blocks
goal_block = f"Goal: {goal}"
goal_type_block = f"Goal Type: {goal_type}"
time_goal_block = f"Time Goal: {time_target} minutes" if time_target else ""
level_block = f"Fitness Level: {level}"
profile_block = f"Age: {age}, Weight: {weight} kg, Height: {height} cm"
injury_block = f"Injuries: {injuries if injuries else 'None'}"

# Construct prompt
prompt = f"""
You are a certified fitness coach.

Create a personalized 4-week fitness plan with the following rules and structure:

1. Every workout must include:
   - A warm-up: Always include this video link - https://www.youtube.com/watch?v=pPlFSqXnbls
   - A main set: Use bullet points. Customize based on the user's goal, level, and injuries.
   - A cool-down: Suggest stretches or activities based on the main workout type (e.g., static stretches for strength, foam rolling for cardio).

2. For beginners:
   - Cardio workouts in Weeks 1 and 2 should alternate between jogging and walking at equal intervals.
   - Total cardio duration should start at 15-20 minutes on Day 1 and gradually increase to 30 minutes by the end of Week 2.

3. If the user has any injury:
   - Avoid high-impact or aggravating exercises.
   - Add low-impact alternatives. Example:
     - For knee injury: seated leg extensions, glute bridges.
     - For shoulder injury: resistance band external rotations.

4. Fitness level adjustments:
   - Beginners: short durations, simple movements, more rest days.
   - Advanced: more intensity, longer sessions, complex workouts.

5. Training goal-specific structure:
   - Runners: include at least 2 strength days and 1 long run per week.
   - Weight loss: include both strength and cardio, spread across the week.
   - General fitness: variety of cardio, bodyweight, and resistance work.

6. Plan structure:
   - Show the plan week-by-week (Week 1 to Week 4).
   - Format as: **Day X: [Label]** followed by structured sections.
   - The plan should get slightly more challenging each week.

User Profile:
{goal_block}
{goal_type_block}
{time_goal_block}
{level_block}
{profile_block}
{injury_block}

Use a friendly and motivating tone. Avoid jargon unless the user is advanced.
"""

# Generate plan
if st.button("Generate Plan"):
    with st.spinner("Generating your plan..."):
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        st.session_state.plan = response.choices[0].message.content
        st.session_state.prompt = prompt
        st.success("✅ Plan generated!")

# Show plan if available
if st.session_state.plan:
    st.markdown(st.session_state.plan)

    # Feedback
    st.markdown("#### Do you like the plan?")
    col1, col2 = st.columns(2)

    with col1:
        like = st.button("👍 Yes, I liked it")
    with col2:
        dislike = st.button("👎 Not quite right")

    if dislike:
        st.markdown("You can try regenerating the plan with the same inputs:")
        if st.button("🔄 Regenerate Plan"):
            with st.spinner("Regenerating your plan..."):
                retry_response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": st.session_state.prompt}],
                    temperature=0.9,
                )
                st.session_state.plan = retry_response.choices[0].message.content
                st.success("✅ Regenerated plan!")
                st.markdown(st.session_state.plan)

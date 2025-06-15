import streamlit as st
import openai
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

st.set_page_config(
    page_title="Vindr - AI Fitness Coach | Personalized Training Plans",
    page_icon="ZeeResizer.png",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://vindr.in',
        'Report a bug': None,
        'About': "Vindr AI Fitness Coach - Get personalized 4-week training plans powered by AI"
    }
)

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Vindr AI Fitness Coach")

# Initialize session state for plan and prompt
if "plan" not in st.session_state:
    st.session_state.plan = None
if "prompt" not in st.session_state:
    st.session_state.prompt = None

# Helper function to get formatted dates
def get_training_dates():
    """Generate 28 days of training dates starting from tomorrow"""
    start_date = datetime.now() + timedelta(days=1)  # Start tomorrow
    dates = []
    for i in range(28):  # 4 weeks = 28 days
        date = start_date + timedelta(days=i)
        dates.append(date.strftime("%d/%m/%Y"))
    return dates

# Collect inputs
st.markdown("### 👤 Your Information")

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

# Get training dates
training_dates = get_training_dates()

# Build modular blocks
goal_block = f"Goal: {goal}"
goal_type_block = f"Goal Type: {goal_type}"
time_goal_block = f"Time Goal: {time_target} minutes" if time_target else ""
level_block = f"Fitness Level: {level}"
profile_block = f"Age: {age}, Weight: {weight} kg, Height: {height} cm"
injury_block = f"Injuries: {injuries if injuries else 'None'}"

# Construct improved prompt with specific date formatting
prompt = f"""
You are a certified fitness coach creating a personalized 4-week fitness plan.

CRITICAL FORMATTING RULES:
1. Use EXACTLY this markdown table format for workout days:
   | Date | Section | Description |
   |------|---------|-------------|
   | DD/MM/YYYY | Warm-up | Description here |
   | DD/MM/YYYY | Main Set | Description here |
   | DD/MM/YYYY | Cool Down | Description here |

2. For REST DAYS, use this format:
   ## Day X: DD/MM/YYYY - REST DAY
   Complete rest or light activity like:
   - 10-15 minute easy walk
   - 5-10 minutes of gentle stretching
   - Foam rolling if available

3. WARM-UP RULES:
   - Always include: "Follow this warm-up routine: https://www.youtube.com/watch?v=pPlFSqXnbls"
   - Add 1-2 specific warm-up exercises

4. MAIN SET RULES:
   - Use bullet points with clear, specific exercises
   - Include sets, reps, or time durations
   - Be specific about intensity levels

5. COOL DOWN RULES:
   - Always include relevant stretches
   - Mention foam rolling when appropriate
   - 5-10 minutes duration

6. TRAINING DATES TO USE (in exact order):
   Week 1: {', '.join(training_dates[0:7])}
   Week 2: {', '.join(training_dates[7:14])}
   Week 3: {', '.join(training_dates[14:21])}
   Week 4: {', '.join(training_dates[21:28])}

7. PROGRESSION RULES:
   - Beginners: Weeks 1-2 should be cardio (jog + walk intervals), 15-20 mins progressing to 30 mins
   - Include 2 strength days + 1 long run per week for runners
   - Weight loss goals need mix of strength + cardio
   - Adapt all exercises if injuries are mentioned

8. Use encouraging, motivating language throughout.

User Profile:
{goal_block}
{goal_type_block}
{time_goal_block}
{level_block}
{profile_block}
{injury_block}

Create the complete 4-week plan with proper formatting and real dates.
"""

# Generate plan
if st.button("🚀 Generate Plan", use_container_width=True):
    if not name or not goal:
        st.error("Please fill in your name and fitness goal!")
    else:
        with st.spinner("Generating your personalized plan..."):
            try:
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )
                st.session_state.plan = response.choices[0].message.content
                st.session_state.prompt = prompt
                st.success("✅ Your fitness plan is ready!")
            except Exception as e:
                st.error(f"Error generating plan: {str(e)}")

# Show plan if available
if st.session_state.plan:
    st.markdown("---")
    st.markdown("## 🏃‍♂️ Your Personalized Fitness Plan")
    
    # Display the plan with proper formatting
    st.markdown(st.session_state.plan)

    # Feedback section
    st.markdown("---")
    st.markdown("### 📝 How's the plan?")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("👍 Love it!", use_container_width=True):
            st.success("Great! Save this plan and start your fitness journey!")
    
    with col2:
        if st.button("🔄 Regenerate", use_container_width=True):
            with st.spinner("Creating a new version..."):
                try:
                    retry_response = openai.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": st.session_state.prompt}],
                        temperature=0.9,  # Higher temperature for more variation
                    )
                    st.session_state.plan = retry_response.choices[0].message.content
                    st.success("✅ New plan generated!")
                    st.rerun()  # Refresh to show new plan
                except Exception as e:
                    st.error(f"Error regenerating plan: {str(e)}")
    
    with col3:
        # Download as text file
        st.download_button(
            label="📥 Download Plan",
            data=st.session_state.plan,
            file_name=f"{name.replace(' ', '_')}_fitness_plan.txt",
            mime="text/plain",
            use_container_width=True
        )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 14px; margin-top: 2rem;'>
        Built with ❤️ by Arun Subramanian | Vindr AI Fitness Coach
    </div>
    """, 
    unsafe_allow_html=True
)
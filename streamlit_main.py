import streamlit as st
import openai
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# SEO-optimized page config
st.set_page_config(
    page_title="Vindr - AI Fitness Coach | Free Personalized Workout Plans & Half Marathon Training Plans",
    page_icon="ZeeResizer.png",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://vindr.in',
        'Report a bug': None,
        'About': "Vindr AI Fitness Coach - Get personalized 4-week training plans powered by AI. Free fitness plan generator for running, strength training, and weight loss goals."
    }
)

# SEO Meta Tags and Open Graph
st.markdown("""
<meta name="description" content="Free AI-powered fitness coach that creates personalized 4-week workout plans. Get custom training programs for running, strength building, weight loss, and general fitness. Start your fitness journey today with Vindr AI Coach.">
<meta name="keywords" content="AI fitness coach, personalized workout plans, free fitness plans, training programs, running plans, strength training, weight loss workouts, 4-week fitness plan, half marathon training plans">
<meta name="author" content="Arun Subramanian">
<meta name="robots" content="index, follow">

<!-- Open Graph / Facebook -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://vindr.in/">
<meta property="og:title" content="Vindr - AI Fitness Coach | Free Personalized Workout Plans">
<meta property="og:description" content="Get your personalized 4-week fitness plan in minutes. AI-powered training programs for running, strength, and weight loss. 100% free.">
<meta property="og:image" content="https://vindr.in/ZeeResizer.png">

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="https://vindr.in/">
<meta property="twitter:title" content="Vindr - AI Fitness Coach | Free Personalized Workout Plans">
<meta property="twitter:description" content="Get your personalized 4-week fitness plan in minutes. AI-powered training programs for running, strength, and weight loss. 100% free.">
<meta property="twitter:image" content="https://vindr.in/ZeeResizer.png">

<!-- Structured Data -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "Vindr AI Fitness Coach",
  "description": "AI-powered fitness coach that creates personalized 4-week workout plans for running, strength training, and weight loss",
  "url": "https://vindr.in",
  "applicationCategory": "HealthApplication",
  "operatingSystem": "Web",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  },
  "author": {
    "@type": "Person",
    "name": "Arun Subramanian"
  }
}
</script>
""", unsafe_allow_html=True)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0 2rem 0;
        border-bottom: 2px solid #f0f2f6;
        margin-bottom: 2rem;
    }
    
    .section-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1f2937;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #e5e7eb;
    }
    
    .stTextInput > div > div > input {
        background-color: #f9fafb;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    .stSelectbox > div > div > div {
        background-color: #f9fafb;
        border-radius: 8px;
    }
    
    .stNumberInput > div > div > input {
        background-color: #f9fafb;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 0.75rem;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
    }
    
    .plan-container {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .feedback-section {
        background-color: #fff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 2rem 0;
    }
    
    /* Make tables more readable */
    .stMarkdown table {
        border-collapse: collapse;
        margin: 1rem 0;
        font-size: 0.95rem;
    }
    
    .stMarkdown th {
        background-color: #f3f4f6;
        padding: 0.75rem;
        text-align: left;
        border: 1px solid #d1d5db;
        font-weight: 600;
    }
    
    .stMarkdown td {
        padding: 0.75rem;
        border: 1px solid #d1d5db;
        vertical-align: top;
    }
    /* Mobile-responsive tables */
    @media (max-width: 768px) {
    .main-header {
        padding: 0.5rem 0 1rem 0;
        margin-bottom: 1rem;
    }
    .stMarkdown table {
        font-size: 0.75rem;
        width: 100%;
        table-layout: fixed;
    }
    
    .stMarkdown th,
    .stMarkdown td {
        padding: 0.4rem 0.2rem;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    .stMarkdown th:first-child,
    .stMarkdown td:first-child {
        width: 15%;
    }
    
    .stMarkdown th:nth-child(2),
    .stMarkdown td:nth-child(2) {
        width: 20%;
    }
    
    .stMarkdown th:nth-child(3),
    .stMarkdown td:nth-child(3) {
        width: 65%;
    }
}
@media (min-width: 769px) and (max-width: 1024px) {
        .stMarkdown table {
            font-size: 0.85rem;
        }
    }

    @media (max-width: 480px) {
        .stMarkdown table {
            font-size: 0.7rem;
        }
        
        .stMarkdown th,
        .stMarkdown td {
            padding: 0.3rem 0.2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Enhanced main header with SEO-friendly content
st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.title("🏃‍♂️ Vindr AI Fitness Coach")
st.markdown("**Get your personalized 4-week training plan in minutes**")
st.markdown("*Free AI-powered workout plans for running, weight loss, strength training, and half marathon training*")
st.markdown('</div>', unsafe_allow_html=True)

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
st.markdown('<div class="section-header">👤 Your Information</div>', unsafe_allow_html=True)

name = st.text_input("Your Name", placeholder="Enter your full name")
goal = st.text_input("Fitness Goal", placeholder="e.g., run 10k, lose weight, build muscle")

goal_type = st.selectbox(
    "Choose your primary goal",
    ["Run a 5K", "Run a 10K", "Run a Half Marathon (21.1k)", "Run a Marathon (42k)",
     "Weight Loss", "General Fitness", "Strength Building"]
)

time_target = None
if goal_type in ["Run a 5K", "Run a 10K", "Run a Half Marathon (21.1k)", "Run a Marathon (42k)"]:
    time_target = st.text_input("Time goal (in minutes)", placeholder="e.g., 30 for a 30-minute 5K")

level = st.selectbox("Fitness Level", ["Beginner", "Intermediate", "Advanced"])

col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age", min_value=12, max_value=90, value=25)
    weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
with col2:
    height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=170.0)

injuries = st.text_area("Any injuries we should know about?", placeholder="Describe any injuries, limitations, or areas to avoid")

st.markdown("<br>", unsafe_allow_html=True)

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
1. Structure each day as: ## Day X: DD/MM/YYYY - [WORKOUT TYPE]
  Examples: 
  - ## Day 1: 16/06/2025 - Tempo Run
  - ## Day 2: 17/06/2025 - REST DAY
  - ## Day 3: 18/06/2025 - Strength Training

2. For WORKOUT DAYS, follow the day header with this table:
  | Date | Section | Description |
  |------|---------|-------------|
  | DD/MM/YYYY | Warm-up | Description here |
  | DD/MM/YYYY | Main Set | Description here |
  | DD/MM/YYYY | Cool Down | Description here |

3. For REST DAYS, after the day header write:
  Complete rest or light activity like:
  - 10-15 minute easy walk
  - 5-10 minutes of gentle stretching
  - Foam rolling if available

4. WARM-UP RULES:
  - Always include: "Follow this warm-up routine: https://www.youtube.com/watch?v=pPlFSqXnbls"
  - Add 1-2 specific warm-up exercises

5. MAIN SET RULES:
  - Use bullet points with clear, specific exercises
  - Include sets, reps, or time durations
  - Be specific about intensity levels
  - Write each exercise on a separate line using bullet points
  - No HTML tags or escape sequences

6. COOL DOWN RULES:
  - Always include relevant stretches
  - Mention foam rolling when appropriate
  - 5-10 minutes duration

7. TRAINING DATES TO USE (in exact order for Days 1-28):
  Days 1-7: {', '.join(training_dates[0:7])}
  Days 8-14: {', '.join(training_dates[7:14])}
  Days 15-21: {', '.join(training_dates[14:21])}
  Days 22-28: {', '.join(training_dates[21:28])}

8. PROGRESSION RULES:
  - Beginners: Days 1-14 should focus on cardio (jog + walk intervals), 15-20 mins progressing to 30 mins
  - Include 2 strength days + 1 long run per week for runners
  - Weight loss goals need mix of strength + cardio
  - Adapt all exercises if injuries are mentioned

9. NEVER use "Week 1", "Week 2" headers. Only use Day numbers (Day 1 through Day 28).

10. Use encouraging, motivating language throughout.

11. FORMATTING:
 - Never use HTML tags like <br> or escape sequences like \n
 - For line breaks in descriptions, use actual line breaks (press Enter)
 - Use bullet points with - or * for lists
 - Keep descriptions clean and readable without formatting codes

User Profile:
{goal_block}
{goal_type_block}
{time_goal_block}
{level_block}
{profile_block}
{injury_block}

Create the complete 28-day plan with proper formatting and real dates.
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
    st.markdown('<div class="plan-container">', unsafe_allow_html=True)
    st.markdown("## 🎯 Your Personalized Fitness Plan")
    
    # Display the plan with proper formatting
    st.markdown(st.session_state.plan)
    st.markdown('</div>', unsafe_allow_html=True)

    # Feedback section
    st.markdown('<div class="feedback-section">', unsafe_allow_html=True)
    st.markdown("### 💭 How's the plan?")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("👍 Love it!", use_container_width=True):
            st.success("🎉 Awesome! Save this plan and start your fitness journey!")
    
    with col2:
        if st.button("🔄 Try Again", use_container_width=True):
            with st.spinner("Creating a fresh version..."):
                try:
                    retry_response = openai.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": st.session_state.prompt}],
                        temperature=0.9,  # Higher temperature for more variation
                    )
                    st.session_state.plan = retry_response.choices[0].message.content
                    st.success("✨ New plan generated!")
                    st.rerun()  # Refresh to show new plan
                except Exception as e:
                    st.error(f"Error regenerating plan: {str(e)}")
    
    with col3:
        # Download as text file
        st.download_button(
            label="📥 Download",
            data=st.session_state.plan,
            file_name=f"{name.replace(' ', '_')}_fitness_plan.txt" if name else "fitness_plan.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

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
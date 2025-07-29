import streamlit as st
import openai
import os
from datetime import datetime, timedelta, date
from dotenv import load_dotenv
from database import UserDatabase
import re

# Initialize database
db = UserDatabase()

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
    
    /* Progress tracking styles */
    .progress-stats {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
    
    .status-green { 
        background-color: #22c55e; 
        color: white; 
        padding: 0.25rem 0.5rem; 
        border-radius: 4px; 
        font-size: 0.8rem;
        display: inline-block;
    }
    .status-yellow { 
        background-color: #eab308; 
        color: white; 
        padding: 0.25rem 0.5rem; 
        border-radius: 4px; 
        font-size: 0.8rem;
        display: inline-block;
    }
    .status-red { 
        background-color: #ef4444; 
        color: white; 
        padding: 0.25rem 0.5rem; 
        border-radius: 4px; 
        font-size: 0.8rem;
        display: inline-block;
    }
    
    /* Day header styling for better single-line display */
    .day-header {
        font-size: 1.1rem !important;
        margin: 1.5rem 0 0.5rem 0 !important;
        line-height: 1.2 !important;
        color: #1f2937 !important;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        font-weight: 600;
    }
    
    /* Responsive day headers */
    @media (max-width: 768px) {
        .day-header {
            font-size: 0.95rem !important;
            white-space: normal;
            line-height: 1.3 !important;
        }
    }
    
    @media (max-width: 480px) {
        .day-header {
            font-size: 0.85rem !important;
        }
    }
    
    /* Fix text visibility issues */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #f9fafb;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 0.75rem;
        font-size: 1rem;
        color: #1f2937 !important;
    }

    /* Fix selectbox text */
    .stSelectbox > div > div > div > div {
        color: #1f2937 !important;
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
    
    /* Completion tracking button styling */
    .stButton > button[data-testid*="mark"], 
    .stButton > button[data-testid*="change"] {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
        font-size: 0.9rem;
        padding: 0.5rem 1rem;
    }
    
    .stButton > button[data-testid*="completed"],
    .stButton > button[data-testid*="different"], 
    .stButton > button[data-testid*="no_activity"] {
        font-size: 1.2rem;
        padding: 0.4rem;
        min-height: 2.5rem;
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
        width: 100%;
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

# Initialize session state
if "user" not in st.session_state:
    st.session_state.user = None
if "plan" not in st.session_state:
    st.session_state.plan = None
if "prompt" not in st.session_state:
    st.session_state.prompt = None
if "current_plan_id" not in st.session_state:
    st.session_state.current_plan_id = None
if "page" not in st.session_state:
    st.session_state.page = "main"

def show_auth_forms():
    """Display login and registration forms"""
    
    auth_tab1, auth_tab2 = st.tabs(["Login", "Sign Up"])
    
    with auth_tab1:
        st.markdown("### Welcome Back!")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            login_submit = st.form_submit_button("Login", use_container_width=True)
            
            if login_submit:
                if email and password:
                    user = db.authenticate_user(email, password)
                    if user:
                        st.session_state.user = user
                        st.success(f"Welcome back, {user['name']}!")
                        st.rerun()
                    else:
                        st.error("Invalid email or password")
                else:
                    st.error("Please enter both email and password")
    
    with auth_tab2:
        st.markdown("### Create Your Account")
        with st.form("register_form"):
            reg_name = st.text_input("Full Name")
            reg_email = st.text_input("Email")
            reg_password = st.text_input("Password", type="password")
            reg_confirm_password = st.text_input("Confirm Password", type="password")
            
            # Optional profile information
            st.markdown("**Optional Profile Information:**")
            reg_fitness_level = st.selectbox("Fitness Level", ["", "Beginner", "Intermediate", "Advanced"])
            
            col1, col2 = st.columns(2)
            with col1:
                reg_age = st.number_input("Age", min_value=0, max_value=100, value=0)
            with col2:
                reg_weight = st.number_input("Weight (kg)", min_value=0.0, max_value=300.0, value=0.0)
            
            register_submit = st.form_submit_button("Create Account", use_container_width=True)
            
            if register_submit:
                if not all([reg_name, reg_email, reg_password, reg_confirm_password]):
                    st.error("Please fill in all required fields")
                elif reg_password != reg_confirm_password:
                    st.error("Passwords do not match")
                elif len(reg_password) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    # Optional fields - only save if provided
                    fitness_level = reg_fitness_level if reg_fitness_level else None
                    age = reg_age if reg_age > 0 else None
                    weight = reg_weight if reg_weight > 0 else None
                    
                    user_id = db.create_user(
                        reg_email, reg_password, reg_name, 
                        fitness_level, age, weight
                    )
                    
                    if user_id:
                        # Auto-login after registration
                        user = db.authenticate_user(reg_email, reg_password)
                        st.session_state.user = user
                        st.success(f"Account created! Welcome, {reg_name}!")
                        st.rerun()
                    else:
                        st.error("Email already exists. Please try logging in.")

def show_user_info():
    """Display logged-in user information"""
    user = st.session_state.user
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.success(f"👋 Welcome back, **{user['name']}**!")
    
    with col2:
        if st.button("📊 Progress", use_container_width=True):
            st.session_state.page = "progress"
            st.rerun()
    
    with col3:
        if st.button("Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.plan = None
            st.session_state.prompt = None
            st.session_state.current_plan_id = None
            st.session_state.page = "main"
            st.success("Logged out successfully!")
            st.rerun()

def parse_plan_for_dates(plan_text):
    """Parse plan text to extract dates and workouts"""
    lines = plan_text.split('\n')
    workouts = {}
    
    for line in lines:
        # Look for day headers like "## Day X: DD/MM/YYYY - Workout Type"
        if line.startswith('## Day') and ':' in line:
            try:
                # Extract date and workout type
                parts = line.split(':')[1].strip().split(' - ')
                if len(parts) >= 2:
                    date_str = parts[0].strip()
                    workout_type = parts[1].strip()
                    
                    # Parse date
                    day, month, year = date_str.split('/')
                    workout_date = date(int(year), int(month), int(day))
                    
                    workouts[workout_date] = workout_type
            except:
                continue
    
    return workouts

def show_progress_tracking():
    """Display enhanced progress tracking interface with complete date range and previous activity logging"""
    if st.button("← Back to Main", key="back_to_main"):
        st.session_state.page = "main"
        st.rerun()
    
    st.markdown("# 📊 Your Progress Dashboard")
    
    user_id = st.session_state.user['id']
    user_plans = db.get_user_plans(user_id)
    
    if not user_plans:
        st.info("No saved plans yet. Create and save a plan first to track your progress!")
        return
    
    # Plan selection
    plan_options = {plan['id']: f"{plan['name']} ({plan['created_at']})" for plan in user_plans}
    selected_plan_id = st.selectbox("Select a plan to track:", options=list(plan_options.keys()), 
                                   format_func=lambda x: plan_options[x])
    
    if selected_plan_id:
        plan_data = db.get_plan_by_id(selected_plan_id, user_id)
        plan_workouts = parse_plan_for_dates(plan_data)
        
        if not plan_workouts:
            st.warning("Could not parse workout dates from this plan. Please ensure the plan has properly formatted dates.")
            return
        
        # Get plan date range
        plan_start_date = min(plan_workouts.keys())
        plan_end_date = max(plan_workouts.keys())
        today = date.today()
        
        # Get current month stats
        current_date = datetime.now()
        monthly_stats = db.get_monthly_stats(user_id, current_date.year, current_date.month)
        
        # Display monthly stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="status-green">🟢 Green Days: {monthly_stats["green"]}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="status-yellow">🟡 Yellow Days: {monthly_stats["yellow"]}</div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="status-red">🔴 Red Days: {monthly_stats["red"]}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Get existing completion data
        history = db.get_workout_history(user_id, selected_plan_id)
        completion_data = {entry['date']: entry for entry in history}
        
        # Today's workout logging
        if today in plan_workouts and today <= plan_end_date:
            st.markdown("### 📅 Today's Workout")
            planned_workout = plan_workouts[today]
            st.info(f"**Planned:** {planned_workout}")
            
            today_str = today.strftime('%Y-%m-%d')
            existing_today = completion_data.get(today_str)
            
            if existing_today:
                st.success(f"✅ Already logged: {existing_today['completion_type'].replace('_', ' ').title()}")
                if st.button("Change Today's Entry", key="change_today"):
                    st.session_state["edit_today"] = True
                    st.rerun()
            
            # Show today's logging interface
            if not existing_today or st.session_state.get("edit_today", False):
                completion_type = st.radio(
                    "What did you do today?",
                    ["✅ Completed as planned", "🔄 Did something different", "⏭️ No activity today"],
                    key="today_completion"
                )

                actual_activity = None
                if completion_type == "🔄 Did something different":
                    actual_activity = st.text_area(
                        "What did you do instead?",
                        placeholder="e.g., 7km easy run, yoga class, 30min walk, 50 squats, etc.",
                        key="today_activity"
                    )
                
                # Fixed column logic to avoid [1, 0] error
                if st.session_state.get("edit_today", False):
                    col_log, col_cancel = st.columns([1, 1])
                else:
                    col_log = st.container()
                    col_cancel = None
                
                with col_log:
                    if st.button("Log Today's Activity", use_container_width=True):
                        completion_map = {
                            "✅ Completed as planned": "completed_planned",
                            "🔄 Did something different": "different_activity", 
                            "⏭️ No activity today": "no_activity"
                        }
                        
                        status_color = db.log_workout_completion(
                            user_id, selected_plan_id, today, planned_workout,
                            completion_map[completion_type], actual_activity
                        )
                        
                        color_emoji = {"green": "🟢", "yellow": "🟡", "red": "🔴"}
                        st.success(f"Logged! Status: {color_emoji[status_color]} {status_color.title()}")
                        st.session_state["edit_today"] = False
                        st.rerun()
                
                if col_cancel is not None:
                    with col_cancel:
                        if st.button("Cancel", use_container_width=True):
                            st.session_state["edit_today"] = False
                            st.rerun()
        
        # Previous activity logging
        st.markdown("### 📅 Log Previous Activity")
        
        if st.button("📅 Log Previous Activity", use_container_width=True, key="log_previous_btn"):
            st.session_state["show_previous_logger"] = True
            st.rerun()
        
        if st.session_state.get("show_previous_logger", False):
            st.markdown("#### Select a previous date to log:")
            
            # Date picker with validation
            selected_date = st.date_input(
                "Choose date:",
                value=today - timedelta(days=1),
                min_value=plan_start_date,
                max_value=min(today - timedelta(days=1), plan_end_date),
                key="previous_date_picker"
            )
            
            if selected_date in plan_workouts:
                planned_workout_prev = plan_workouts[selected_date]
                st.info(f"**Planned for {selected_date.strftime('%d/%m/%Y')}:** {planned_workout_prev}")
                
                # Check if already logged
                selected_date_str = selected_date.strftime('%Y-%m-%d')
                existing_prev = completion_data.get(selected_date_str)
                
                if existing_prev:
                    st.warning(f"Already logged: {existing_prev['completion_type'].replace('_', ' ').title()}")
                    if existing_prev['actual_activity']:
                        st.write(f"Activity: {existing_prev['actual_activity']}")
                    st.write("You can overwrite this entry:")
                
                # Logging interface for previous date
                prev_completion_type = st.radio(
                    "What did you do on this date?",
                    ["✅ Completed as planned", "🔄 Did something different", "⏭️ No activity"],
                    key="prev_completion"
                )
                
                prev_actual_activity = None
                if prev_completion_type == "🔄 Did something different":
                    prev_actual_activity = st.text_area(
                        "What did you do instead?",
                        placeholder="e.g., 7km easy run, yoga class, 30min walk, 50 squats, etc.",
                        key="prev_activity"
                    )
                
                col_log_prev, col_cancel_prev = st.columns(2)
                print(f"DEBUG: Created columns at line 593")     # ADD THIS LINE
                
                with col_log_prev:
                    if st.button("Log This Activity", use_container_width=True, key="log_prev_submit"):
                        completion_map = {
                            "✅ Completed as planned": "completed_planned",
                            "🔄 Did something different": "different_activity", 
                            "⏭️ No activity": "no_activity"
                        }
                        
                        status_color = db.log_workout_completion(
                            user_id, selected_plan_id, selected_date, planned_workout_prev,
                            completion_map[prev_completion_type], prev_actual_activity
                        )
                        
                        color_emoji = {"green": "🟢", "yellow": "🟡", "red": "🔴"}
                        st.success(f"Logged for {selected_date.strftime('%d/%m/%Y')}! Status: {color_emoji[status_color]} {status_color.title()}")
                        st.session_state["show_previous_logger"] = False
                        st.rerun()
                
                with col_cancel_prev:
                    if st.button("Cancel", use_container_width=True, key="cancel_prev"):
                        st.session_state["show_previous_logger"] = False
                        st.rerun()
            
            elif selected_date <= plan_end_date:
                st.warning(f"No planned workout found for {selected_date.strftime('%d/%m/%Y')}. This might be a rest day.")
            else:
                st.error("Selected date is outside your plan range.")
        
        st.markdown("---")
        
        # Enhanced workout history with complete date range
        st.markdown("### 📋 Complete Workout History")
        
        # Generate complete date range from plan start to today (or plan end, whichever is earlier)
        end_display_date = min(today, plan_end_date)
        current_date_iter = plan_start_date
        complete_history = []
        
        while current_date_iter <= end_display_date:
            date_str = current_date_iter.strftime('%Y-%m-%d')
            display_date = current_date_iter.strftime('%Y-%m-%d')
            
            if date_str in completion_data:
                # Has logged activity
                entry = completion_data[date_str]
                if entry['completion_type'] == 'completed_planned':
                    activity_text = entry['planned_workout']
                elif entry['completion_type'] == 'different_activity':
                    activity_text = entry['actual_activity'] or "Different activity"
                else:
                    activity_text = "No activity"
                
                color_emoji = {"green": "🟢", "yellow": "🟡", "red": "🔴"}
                status_display = color_emoji[entry['status_color']]
                
                complete_history.append({
                    'date': display_date,
                    'activity': activity_text,
                    'status': status_display,
                    'status_color': entry['status_color']
                })
            else:
                # No logged activity
                planned_workout_display = plan_workouts.get(current_date_iter, "Rest Day")
                complete_history.append({
                    'date': display_date,
                    'activity': "Activity Not Logged",
                    'status': "⚪",
                    'status_color': "gray"
                })
            
            current_date_iter += timedelta(days=1)
        
        # Display complete history (most recent first)
        if complete_history:
            # Show last 21 days by default, with option to show all
            display_limit = 21
            
            if len(complete_history) > display_limit:
                show_all = st.checkbox(f"Show all {len(complete_history)} days", key="show_all_history")
                display_history = complete_history if show_all else complete_history[-display_limit:]
            else:
                display_history = complete_history
            
            # Reverse to show most recent first
            display_history.reverse()
            
            for entry in display_history:
                col1, col2, col3 = st.columns([2, 5, 1])
                
                with col1:
                    st.write(f"**{entry['date']}**")
                
                with col2:
                    if entry['activity'] == "Activity Not Logged":
                        st.write(f"*{entry['activity']}*")
                    else:
                        st.write(entry['activity'])
                
                with col3:
                    if entry['status_color'] != "gray":
                        st.markdown(f'<div class="status-{entry["status_color"]}">{entry["status"]}</div>', unsafe_allow_html=True)
                    else:
                        st.write(entry['status'])
        else:
            st.info("No workout history yet. Start logging your workouts!")
        
        # Plan summary
        st.markdown("---")
        st.markdown("### 📈 Plan Summary")
        
        total_plan_days = len(plan_workouts)
        logged_days = len([h for h in complete_history if h['activity'] != "Activity Not Logged"])
        completion_percentage = (logged_days / len(complete_history)) * 100 if complete_history else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Plan Days", total_plan_days)
        with col2:
            st.metric("Days Logged", f"{logged_days}/{len(complete_history)}")
        with col3:
            st.metric("Completion Rate", f"{completion_percentage:.1f}%")

def show_main_page():
    """Display the main fitness plan generation page with inline completion tracking"""
    
    # Helper function to get formatted dates
    def get_training_dates():
        """Generate 28 days of training dates starting from tomorrow"""
        start_date = datetime.now() + timedelta(days=1)  # Start tomorrow
        dates = []
        for i in range(28):  # 4 weeks = 28 days
            date = start_date + timedelta(days=i)
            dates.append(date.strftime("%d/%m/%Y"))
        return dates

    def display_plan_with_completion_tracking():
        """Display the plan with inline completion tracking for each day"""
        if not st.session_state.plan:
            return
        
        user_id = st.session_state.user['id']
        current_plan_id = st.session_state.current_plan_id
        
        # Get existing completion data
        completion_data = {}
        if current_plan_id:
            history = db.get_workout_history(user_id, current_plan_id)
            completion_data = {entry['date']: entry for entry in history}
        
        st.markdown('<div class="plan-container">', unsafe_allow_html=True)
        st.markdown("## 🎯 Your Personalized Fitness Plan")
        
        # Split plan into lines and process each line
        lines = st.session_state.plan.split('\n')
        current_day_info = None
        
        for i, line in enumerate(lines):
            # Check if this is a day header (## Day X: DD/MM/YYYY - Workout Type)
            if line.startswith('## Day') and ':' in line:
                # Extract day information
                try:
                    # Parse: "## Day 1: 05/07/2025 - Cardio (Jog + Walk Intervals)"
                    day_part = line.split(':')[0].replace('## ', '')  # "Day 1"
                    rest_part = ':'.join(line.split(':')[1:]).strip()  # "05/07/2025 - Cardio (Jog + Walk Intervals)"
                    
                    if ' - ' in rest_part:
                        date_str = rest_part.split(' - ')[0].strip()  # "05/07/2025"
                        workout_type = ' - '.join(rest_part.split(' - ')[1:]).strip()  # "Cardio (Jog + Walk Intervals)"
                        
                        # Parse date for database lookup
                        try:
                            day, month, year = date_str.split('/')
                            workout_date = date(int(year), int(month), int(day))
                            date_str_for_db = workout_date.strftime('%Y-%m-%d')
                            
                            current_day_info = {
                                'day': day_part,
                                'date': date_str,
                                'workout_type': workout_type,
                                'workout_date': workout_date,
                                'date_str_for_db': date_str_for_db
                            }
                            
                            # Display day header with smaller font and completion tracking
                            col1, col2 = st.columns([3, 1])
                            
                            with col1:
                                # Use smaller heading with CSS to ensure single line
                                st.markdown(f"""
                                <h4 style='font-size: 1.1rem; margin: 1.5rem 0 0.5rem 0; line-height: 1.2; color: #1f2937; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>
                                    {day_part}: {date_str} - {workout_type}
                                </h4>
                                """, unsafe_allow_html=True)
                            
                            with col2:
                                # Check existing completion status
                                existing_completion = completion_data.get(date_str_for_db)
                                
                                if existing_completion:
                                    # Show current status with color coding
                                    status_color = existing_completion['status_color']
                                    
                                    # Create proper status text with color coding
                                    if existing_completion['completion_type'] == 'completed_planned':
                                        status_text = "✅ Completed"
                                        status_class = f"status-{status_color}"
                                    elif existing_completion['completion_type'] == 'different_activity':
                                        # Show color-appropriate emoji based on actual status_color from database
                                        if status_color == 'green':
                                            status_text = "🟢 Different"
                                        elif status_color == 'yellow':
                                            status_text = "🟡 Different"
                                        else:
                                            status_text = "🔴 Different"
                                        status_class = f"status-{status_color}"
                                    else:  # no_activity
                                        status_text = "🔴 No Activity"
                                        status_class = f"status-{status_color}"
                                    
                                    st.markdown(f'<div class="{status_class}" style="text-align: center; margin-top: 1rem; font-size: 0.8rem;">{status_text}</div>', 
                                              unsafe_allow_html=True)
                                    
                                    # Add option to change status
                                    if st.button(f"Change", key=f"change_{date_str_for_db}", use_container_width=True):
                                        st.session_state[f"show_completion_{date_str_for_db}"] = True
                                        st.rerun()
                                else:
                                    # Show mark complete button
                                    if st.button(f"Mark Complete", key=f"mark_{date_str_for_db}", use_container_width=True):
                                        st.session_state[f"show_completion_{date_str_for_db}"] = True
                                        st.rerun()
                                
                                # Show completion options if triggered
                                if st.session_state.get(f"show_completion_{date_str_for_db}", False):
                                    st.markdown("**Mark as:**")
                                    
                                    col_a, col_b, col_c = st.columns(3)
                                    
                                    with col_a:
                                        if st.button("✅", key=f"completed_{date_str_for_db}", 
                                                   help="Completed as planned", use_container_width=True):
                                            if current_plan_id:
                                                db.log_workout_completion(
                                                    user_id, current_plan_id, workout_date, 
                                                    workout_type, "completed_planned"
                                                )
                                                st.session_state[f"show_completion_{date_str_for_db}"] = False
                                                st.success("✅ Marked as completed!")
                                                st.rerun()
                                    
                                    with col_b:
                                        if st.button("🔄", key=f"different_{date_str_for_db}", 
                                                   help="Did something different", use_container_width=True):
                                            st.session_state[f"show_different_{date_str_for_db}"] = True
                                            st.rerun()
                                    
                                    with col_c:
                                        if st.button("⏭️", key=f"no_activity_{date_str_for_db}", 
                                                   help="No activity today", use_container_width=True):
                                            if current_plan_id:
                                                db.log_workout_completion(
                                                    user_id, current_plan_id, workout_date, 
                                                    workout_type, "no_activity"
                                                )
                                                st.session_state[f"show_completion_{date_str_for_db}"] = False
                                                st.success("Logged: No activity")
                                                st.rerun()
                                    
                                    # Handle "different activity" input
                                    if st.session_state.get(f"show_different_{date_str_for_db}", False):
                                        different_activity = st.text_input(
                                            "What did you do instead?",
                                            placeholder="e.g., 7km easy run, yoga class, 30min walk",
                                            key=f"activity_input_{date_str_for_db}"
                                        )
                                        
                                        col_save, col_cancel = st.columns(2)
                                        with col_save:
                                            if st.button("Save", key=f"save_different_{date_str_for_db}"):
                                                if different_activity and current_plan_id:
                                                    db.log_workout_completion(
                                                        user_id, current_plan_id, workout_date, 
                                                        workout_type, "different_activity", different_activity
                                                    )
                                                    st.session_state[f"show_completion_{date_str_for_db}"] = False
                                                    st.session_state[f"show_different_{date_str_for_db}"] = False
                                                    st.success("🔄 Logged different activity!")
                                                    st.rerun()
                                        
                                        with col_cancel:
                                            if st.button("Cancel", key=f"cancel_different_{date_str_for_db}"):
                                                st.session_state[f"show_different_{date_str_for_db}"] = False
                                                st.rerun()
                                    
                                    # Cancel button for main completion selection
                                    if st.button("Cancel", key=f"cancel_{date_str_for_db}", use_container_width=True):
                                        st.session_state[f"show_completion_{date_str_for_db}"] = False
                                        st.rerun()
                            
                        except (ValueError, IndexError):
                            # If date parsing fails, just show the original line
                            st.markdown(line)
                            current_day_info = None
                    else:
                        # If no workout type found, show original line
                        st.markdown(line)
                        current_day_info = None
                        
                except (IndexError, ValueError):
                    # If parsing fails, show original line
                    st.markdown(line)
                    current_day_info = None
            else:
                # For non-day-header lines, just display as markdown
                st.markdown(line)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Collect inputs - pre-fill with user data if available
    st.markdown('<div class="section-header">👤 Your Information</div>', unsafe_allow_html=True)

    user = st.session_state.user
    name = st.text_input("Your Name", value=user['name'], placeholder="Enter your full name")
    goal = st.text_input("Fitness Goal", placeholder="e.g., run 10k, lose weight, build muscle")

    goal_type = st.selectbox(
        "Choose your primary goal",
        ["Run a 5K", "Run a 10K", "Run a Half Marathon (21.1k)", "Run a Marathon (42k)",
         "Weight Loss", "General Fitness", "Strength Building"],
        index=0 if not user.get('fitness_level') else (
            ["Beginner", "Intermediate", "Advanced"].index(user['fitness_level']) 
            if user['fitness_level'] in ["Beginner", "Intermediate", "Advanced"] else 0
        )
    )

    time_target = None
    if goal_type in ["Run a 5K", "Run a 10K", "Run a Half Marathon (21.1k)", "Run a Marathon (42k)"]:
        time_target = st.text_input("Time goal (in minutes)", placeholder="e.g., 30 for a 30-minute 5K")

    level = st.selectbox(
        "Fitness Level", 
        ["Beginner", "Intermediate", "Advanced"],
        index=0 if not user.get('fitness_level') else (
            ["Beginner", "Intermediate", "Advanced"].index(user['fitness_level']) 
            if user['fitness_level'] in ["Beginner", "Intermediate", "Advanced"] else 0
        )
    )

    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=12, max_value=90, value=user['age'] if user.get('age') else 25)
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=user['weight'] if user.get('weight') else 70.0)
    with col2:
        height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=user['height'] if user.get('height') else 170.0)

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

    # Show plan with inline completion tracking if available
    if st.session_state.plan:
        display_plan_with_completion_tracking()

        # Feedback section with save functionality
        st.markdown('<div class="feedback-section">', unsafe_allow_html=True)
        st.markdown("### 💭 How's the plan?")
        
        # Add save plan functionality
        plan_name = st.text_input("Save this plan as:", placeholder="e.g., My 5K Training Plan")
        
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        
        with col1:
            if st.button("💾 Save Plan", use_container_width=True):
                if plan_name:
                    plan_id = db.save_user_plan(user['id'], plan_name, st.session_state.plan)
                    st.session_state.current_plan_id = plan_id
                    st.success(f"✅ Plan saved as '{plan_name}'!")
                else:
                    st.error("Please enter a plan name")
        
        with col2:
            if st.button("👍 Love it!", use_container_width=True):
                st.success("🎉 Awesome! Don't forget to save your plan!")
        
        with col3:
            if st.button("🔄 Try Again", use_container_width=True):
                with st.spinner("Creating a fresh version..."):
                    try:
                        retry_response = openai.chat.completions.create(
                            model="gpt-4o",
                            messages=[{"role": "user", "content": st.session_state.prompt}],
                            temperature=0.9,
                        )
                        st.session_state.plan = retry_response.choices[0].message.content
                        st.success("✨ New plan generated!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error regenerating plan: {str(e)}")
        
        with col4:
            # Download as text file
            st.download_button(
                label="📥 Download",
                data=st.session_state.plan,
                file_name=f"{name.replace(' ', '_')}_fitness_plan.txt" if name else "fitness_plan.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Display user's saved plans
    if st.session_state.user:
        user_plans = db.get_user_plans(st.session_state.user['id'])
        if user_plans:
            st.markdown("### 📁 Your Saved Plans")
            for plan in user_plans:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{plan['name']}** - {plan['created_at']}")
                with col2:
                    if st.button(f"Load", key=f"load_{plan['id']}", use_container_width=True):
                        plan_data = db.get_plan_by_id(plan['id'], st.session_state.user['id'])
                        if plan_data:
                            st.session_state.plan = plan_data
                            st.session_state.current_plan_id = plan['id']
                            st.success(f"Loaded '{plan['name']}'!")
                            st.rerun()

# Enhanced main header with SEO-friendly content
st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.title("🏃‍♂️ Vindr AI Fitness Coach")
st.markdown("**Get your personalized 4-week training plan in minutes**")
st.markdown("*Free AI-powered workout plans for running, weight loss, strength training, and half marathon training*")
st.markdown('</div>', unsafe_allow_html=True)

# Authentication check
if not st.session_state.user:
    st.markdown("### 🔐 Login or Sign Up to Get Started")
    st.markdown("Create your free account to save your fitness plans and track your progress!")
    show_auth_forms()
    st.stop()

# Show user info if logged in
show_user_info()

# Page routing
if st.session_state.page == "progress":
    show_progress_tracking()
else:
    show_main_page()

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
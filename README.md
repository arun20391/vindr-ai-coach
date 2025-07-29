# Vindr AI Fitness Coach 🏃‍♂️

**AI-powered personalized fitness coaching platform with WhatsApp integration**

Vindr generates personalized 4-week workout plans using OpenAI's GPT-4 and provides comprehensive progress tracking. Users can mark workout completions directly in their plans and track their fitness journey with intelligent color-coded analytics.

## ✨ Current Features

### 🎯 **Plan Generation**
- **Personalized 4-week fitness plans** tailored to user goals (5K, 10K, half marathon, strength, weight loss)
- **Goal-specific training** with proper progression and periodization
- **Injury-aware planning** that adapts to user limitations
- **Multiple plan storage** - save and load different training programs

### 👤 **User Management**
- **Secure authentication** with bcrypt password hashing
- **User profiles** with fitness metrics (age, weight, height, fitness level)
- **Session persistence** - stay logged in across visits
- **Profile customization** for better plan personalization

### 📊 **Progress Tracking**
- **Inline completion tracking** - mark workouts complete directly in your plan
- **Smart color coding**:
  - 🟢 **Green**: Completed as planned or high-effort alternative activities
  - 🟡 **Yellow**: Light activities (short walks, minimal exercise)
  - 🔴 **Red**: No activity logged
- **Complete date history** - view every day from plan start with no gaps
- **Previous activity logging** - retroactively log missed workouts with date picker
- **Progress dashboard** with monthly statistics and streak tracking

### 💡 **Smart Features**
- **Intelligent activity classification** - automatically determines workout intensity
- **Plan persistence** - all plans saved to database with timestamps
- **Mobile-responsive design** - works seamlessly on all devices
- **SEO optimized** - discoverable via search engines

## 🛠 Tech Stack

- **Backend**: Python 3.11+, SQLite, bcrypt
- **Frontend**: Streamlit with custom CSS
- **AI**: OpenAI GPT-4 API
- **Database**: SQLite with comprehensive user and workout tracking
- **Deployment**: Ready for production deployment

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd vindr-ai-coach
   ```

2. **Set up environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Add your OpenAI API key to .env
   OPENAI_API_KEY=your_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run streamlit_main.py
   ```

5. **Access the app**
   - Open your browser to `http://localhost:8501`
   - Create an account and start generating personalized fitness plans!

## 📱 Coming Next: WhatsApp Integration

**Phase 3 (Next 15 days)** - Revolutionary conversational fitness coaching:

### 🎯 **Upcoming Features**
- **Daily WhatsApp reminders** with personalized workout notifications
- **Conversational AI coach** - ask questions, get instant responses
- **Smart nudging** - motivation and micro-workout suggestions
- **Progress tracking via chat** - mark completions through WhatsApp
- **Exercise guidance** - form tips and technique advice on demand

### 💬 **WhatsApp Use Cases**
```
User: "How do I do squats?"
Vindr: "Here's proper squat form: Keep feet shoulder-width apart..."

User: "I missed today's workout"
Vindr: "No worries! Try 10 squats + 5 push-ups to keep momentum going 💪"

User: "I only have 15 minutes"
Vindr: "Perfect! Here's a quick HIIT session: 30sec jumping jacks..."
```

## 🗺 Development Roadmap

- ✅ **Phase 1-2**: Foundation & User System (Complete)
- 🎯 **Phase 3**: WhatsApp Integration (In Progress - 15 days)
- 📹 **Phase 4**: Video Integration (3 weeks)
- 📊 **Phase 5**: Garmin Analytics (3-4 weeks)

## 🏗 Architecture

```
┌─ streamlit_main.py    # Main web application
├─ database.py          # User auth & workout tracking
├─ requirements.txt     # Python dependencies
└─ roadmap.md          # Detailed development plan
```

### 🗄 **Database Schema**
- **Users**: Authentication, profiles, preferences
- **User Plans**: Saved workout plans with timestamps
- **Workout Completions**: Activity tracking with intelligent color coding

## 🤝 Contributing

This is a personal learning project documenting a 90-day fitness app development journey. 

**Current Focus**: Building WhatsApp Business API integration for conversational fitness coaching.

## 📊 Metrics & Analytics

- **Smart completion tracking** with green/yellow/red color coding
- **Progress visualization** with monthly statistics
- **Plan completion rates** and streak tracking
- **User engagement** metrics across web and (soon) WhatsApp

## 🎖 Success Stories

*Vindr helps users stay consistent with personalized coaching and intelligent progress tracking. The upcoming WhatsApp integration will make fitness coaching as accessible as sending a text message.*

---

**Built with ❤️ and discipline by Arun Subramanian**

*Follow the journey: From CLI tool → Web app → WhatsApp AI coach → Complete fitness ecosystem*

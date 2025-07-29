import sqlite3
import bcrypt
from datetime import datetime, date
import os
import re

class UserDatabase:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                fitness_level TEXT,
                age INTEGER,
                weight REAL,
                height REAL
            )
        ''')
        
        # User plans table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                plan_name TEXT NOT NULL,
                plan_data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Workout completions table - NEW
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workout_completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                plan_id INTEGER NOT NULL,
                workout_date DATE NOT NULL,
                planned_workout TEXT NOT NULL,
                completion_type TEXT NOT NULL,
                actual_activity TEXT,
                status_color TEXT NOT NULL,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (plan_id) REFERENCES user_plans (id),
                UNIQUE(user_id, plan_id, workout_date)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """Hash a password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    def verify_password(self, password, hashed):
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed)
    
    def create_user(self, email, password, name, fitness_level=None, age=None, weight=None, height=None):
        """Create a new user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            password_hash = self.hash_password(password)
            cursor.execute('''
                INSERT INTO users (email, password_hash, name, fitness_level, age, weight, height)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (email, password_hash, name, fitness_level, age, weight, height))
            
            user_id = cursor.lastrowid
            conn.commit()
            return user_id
        except sqlite3.IntegrityError:
            return None  # User already exists
        finally:
            conn.close()
    
    def authenticate_user(self, email, password):
        """Authenticate a user and return user info if successful"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, email, password_hash, name, fitness_level, age, weight, height FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        
        if user and self.verify_password(password, user[2]):
            # Update last login
            cursor.execute('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?', (user[0],))
            conn.commit()
            
            # Return user info (without password hash)
            return {
                'id': user[0],
                'email': user[1],
                'name': user[3],
                'fitness_level': user[4],
                'age': user[5],
                'weight': user[6],
                'height': user[7]
            }
        
        conn.close()
        return None
    
    def get_user_by_id(self, user_id):
        """Get user information by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, email, name, fitness_level, age, weight, height FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'email': user[1],
                'name': user[2],
                'fitness_level': user[3],
                'age': user[4],
                'weight': user[5],
                'height': user[6]
            }
        return None
    
    def save_user_plan(self, user_id, plan_name, plan_data):
        """Save a fitness plan for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO user_plans (user_id, plan_name, plan_data)
            VALUES (?, ?, ?)
        ''', (user_id, plan_name, plan_data))
        
        plan_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return plan_id
    
    def get_user_plans(self, user_id):
        """Get all plans for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, plan_name, created_at FROM user_plans 
            WHERE user_id = ? ORDER BY created_at DESC
        ''', (user_id,))
        
        plans = cursor.fetchall()
        conn.close()
        
        return [{'id': plan[0], 'name': plan[1], 'created_at': plan[2]} for plan in plans]
    
    def get_plan_by_id(self, plan_id, user_id):
        """Get a specific plan by ID (with user verification)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT plan_data FROM user_plans 
            WHERE id = ? AND user_id = ?
        ''', (plan_id, user_id))
        
        plan = cursor.fetchone()
        conn.close()
        
        return plan[0] if plan else None
    
    def determine_status_color(self, completion_type, actual_activity=None):
        """Determine the status color based on completion type and activity"""
        if completion_type == "completed_planned":
            return "green"
        elif completion_type == "no_activity":
            return "red"
        elif completion_type == "different_activity":
            if not actual_activity:
                return "red"
            
            # Analyze the activity text to determine green vs yellow
            activity_lower = actual_activity.lower()
            
            # Green criteria (full effort) - IMPROVED
            green_keywords = [
                "gym", "workout", "training", "run", "ran", "jog", "jogged", "bike", "biked", "cycle", "cycled", "swim", "swam",
                "strength", "weights", "cardio", "yoga", "pilates", "hiit", "crossfit", "lift", "lifted", "squat", "squats",
                "pushup", "pushups", "push-up", "push-ups", "burpee", "burpees", "plank", "planks"
            ]
            
            # Check for distance indicators (km, miles, meters)
            distance_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:km|k|mile|miles|meter|meters|m)', activity_lower)
            if distance_match:
                distance = float(distance_match.group(1))
                # If distance >= 3km or >= 2 miles, it's green
                if ('km' in activity_lower or 'k' in activity_lower) and distance >= 3:
                    return "green"
                elif ('mile' in activity_lower) and distance >= 2:
                    return "green"
                elif ('meter' in activity_lower or 'm' in activity_lower) and distance >= 3000:
                    return "green"
            
            # Check for duration >= 30 minutes
            duration_match = re.search(r'(\d+)\s*(?:min|minute|minutes|hour|hours|hr)', activity_lower)
            if duration_match:
                duration = int(duration_match.group(1))
                if "hour" in activity_lower or "hr" in activity_lower:
                    duration *= 60
                if duration >= 30:
                    return "green"
            
            # Check for high rep counts (>=50)
            rep_matches = re.findall(r'(\d+)\s*(?:pushup|squat|burpee|rep|reps|time)', activity_lower)
            if rep_matches:
                total_reps = sum(int(rep) for rep in rep_matches)
                if total_reps >= 50:
                    return "green"
            
            # Check for green keywords
            if any(keyword in activity_lower for keyword in green_keywords):
                return "green"
            
            # Check for walking with sufficient duration
            if "walk" in activity_lower:
                if duration_match and int(duration_match.group(1)) >= 25:
                    return "green"
                else:
                    return "yellow"
            
            # Default to yellow for light activity
            return "yellow"
        
        return "red"
    
    def log_workout_completion(self, user_id, plan_id, workout_date, planned_workout, completion_type, actual_activity=None):
        """Log a workout completion"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        status_color = self.determine_status_color(completion_type, actual_activity)
        
        # Use REPLACE to handle duplicates (user changing their mind about same day)
        cursor.execute('''
            REPLACE INTO workout_completions 
            (user_id, plan_id, workout_date, planned_workout, completion_type, actual_activity, status_color)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, plan_id, workout_date, planned_workout, completion_type, actual_activity, status_color))
        
        conn.commit()
        conn.close()
        
        return status_color
    
    def get_workout_history(self, user_id, plan_id=None):
        """Get workout completion history for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if plan_id:
            cursor.execute('''
                SELECT workout_date, planned_workout, completion_type, actual_activity, status_color
                FROM workout_completions 
                WHERE user_id = ? AND plan_id = ?
                ORDER BY workout_date DESC
            ''', (user_id, plan_id))
        else:
            cursor.execute('''
                SELECT workout_date, planned_workout, completion_type, actual_activity, status_color
                FROM workout_completions 
                WHERE user_id = ?
                ORDER BY workout_date DESC
            ''', (user_id,))
        
        completions = cursor.fetchall()
        conn.close()
        
        return [{
            'date': completion[0],
            'planned_workout': completion[1],
            'completion_type': completion[2],
            'actual_activity': completion[3],
            'status_color': completion[4]
        } for completion in completions]
    
    def get_monthly_stats(self, user_id, year, month):
        """Get monthly stats for color-coded calendar"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT status_color, COUNT(*) as count
            FROM workout_completions 
            WHERE user_id = ? 
            AND strftime('%Y', workout_date) = ? 
            AND strftime('%m', workout_date) = ?
            GROUP BY status_color
        ''', (user_id, str(year), str(month).zfill(2)))
        
        stats = cursor.fetchall()
        conn.close()
        
        result = {'green': 0, 'yellow': 0, 'red': 0}
        for stat in stats:
            result[stat[0]] = stat[1]
        
        return result
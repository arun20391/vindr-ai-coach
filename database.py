import sqlite3
import bcrypt
from datetime import datetime
import os

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
        
        # User progress table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                plan_id INTEGER NOT NULL,
                workout_date DATE NOT NULL,
                completed BOOLEAN DEFAULT FALSE,
                notes TEXT,
                completed_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (plan_id) REFERENCES user_plans (id)
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
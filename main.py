import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

name = input("Enter your name: ")
goal = input("What's your fitness goal? (e.g., run 10k, build muscle, lose fat): ")
level = input("Your fitness level (beginner, intermediate, advanced): ")
weight = input("Your weight in kg: ")
height = input("Your height in cm: ")
age = input("Your age: ")

prompt = f"""Generate a 4-week fitness plan for a {level} individual.
Details:
Name: {name}
Goal: {goal}
Weight: {weight} kg
Height: {height} cm
Age: {age}
The plan should be specific, weekly, and goal-oriented. Include atleast 2 weeks of strength if the goal is run oriented. Include atleast 2 sessions of cardio even if the goal is strength oriented."""

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7,
)

print("\n🏋️ Your Personalized Fitness Plan:\n")
print(response.choices[0].message.content.strip())

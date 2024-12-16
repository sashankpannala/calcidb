import os
import sys
import json
import requests
from dotenv import load_dotenv
from models import User, Session, Base
from sqlalchemy import Column, Integer, String
from faker import Faker

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

# Validate API Key
if not API_KEY:
    raise ValueError("API_KEY not found. Please check your .env file.")

# Initialize Faker and SQLAlchemy Session
session = Session()
fake = Faker()

# Define CalculationHistory model
class CalculationHistory(Base):
    __tablename__ = 'calculation_history'
    id = Column(Integer, primary_key=True)
    calculation = Column(String, nullable=False)
    result = Column(String, nullable=False)

    def __repr__(self):
        return f"<CalculationHistory(id={self.id}, calculation='{self.calculation}', result='{self.result}')>"

# Create tables if not already created
Base.metadata.create_all(session.bind)

# Seed the database with users
for _ in range(5):
    user = User(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.unique.email(),
        username=fake.unique.user_name()
    )
    session.add(user)

session.commit()
print("Database seeded successfully!")

# Define calculator functions
def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b): return a / b if b != 0 else "Error: Division by zero"

# Call Groq API for LLM function calling
def call_llm(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "functions": [
            {"name": "add", "parameters": {"a": "number", "b": "number"}},
            {"name": "subtract", "parameters": {"a": "number", "b": "number"}},
            {"name": "multiply", "parameters": {"a": "number", "b": "number"}},
            {"name": "divide", "parameters": {"a": "number", "b": "number"}}
        ]
    }

    try:
        response = requests.post(API_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        function_calls = data['choices'][0]['message'].get('tool_calls', None)
        if function_calls:
            try:
                function_name = function_calls[0]['function']['name']
                arguments = json.loads(function_calls[0]['function']['arguments'])
                a = float(arguments['a'])
                b = float(arguments['b'])
            except (ValueError, TypeError, KeyError, json.JSONDecodeError):
                return "Error: Invalid arguments or function name in API response."

            if function_name == "add":
                return f"The sum of {a} and {b} is {add(a, b)}."
            elif function_name == "subtract":
                return f"The difference between {a} and {b} is {subtract(a, b)}."
            elif function_name == "multiply":
                return f"The product of {a} and {b} is {multiply(a, b)}."
            elif function_name == "divide":
                return f"The result of dividing {a} by {b} is {divide(a, b)}."
            else:
                return "Error: Function not implemented."

        return "Error: No valid function call in response."
    except requests.exceptions.RequestException as e:
        return f"Error calling Groq API: {e}"

# Save calculation history to the database
def save_history(calculation, result):
    with Session() as session:
        history_entry = CalculationHistory(calculation=calculation, result=result)
        session.add(history_entry)
        session.commit()
    print("Calculation saved to history.")

# Display calculation history from the database
def display_history():
    with Session() as session:
        history = session.query(CalculationHistory).all()
        if not history:
            print("No calculation history available.")
        else:
            print("Calculation History:")
            for entry in history:
                print(f"{entry.id}. {entry.calculation} -> {entry.result}")

# Main function
def main():
    print("Database seeded successfully! Now ready for calculations.")

    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        print(f"Command-line input detected: {prompt}")
        result = call_llm(prompt)
        if result:
            print(f"Result: {result}")
            save_history(prompt, result)
        return

    calc_prompt = os.getenv("CALC_PROMPT")
    if calc_prompt:
        print(f"Using CALC_PROMPT: {calc_prompt}")
        result = call_llm(calc_prompt)
        if result:
            print(f"Result: {result}")
            save_history(calc_prompt, result)
        return

    if sys.stdin.isatty():
        try:
            while True:
                prompt = input("Enter a calculation (e.g., Add 5 and 3), 'history', or 'exit': ")
                if prompt.lower() == "exit":
                    print("Goodbye!")
                    break
                elif prompt.lower() == "history":
                    display_history()
                else:
                    result = call_llm(prompt)
                    if result:
                        print(f"Result: {result}")
                        save_history(prompt, result)
        except EOFError:
            print("\nNo input provided. Exiting.")
    else:
        print("No input provided. Use command-line arguments or the CALC_PROMPT environment variable.")

if __name__ == "__main__":
    main()

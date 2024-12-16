import os
import sys
import json
import random
import requests
from dotenv import load_dotenv
from models import User, Session, Base
from sqlalchemy import Column, Integer, String
from faker import Faker
from word2number import w2n

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

# Fetch user details by email
def fetch_user_by_email(email):
    user = session.query(User).filter(User.email == email).first()
    if user:
        return {"first_name": user.first_name, "last_name": user.last_name, "email": user.email, "username": user.username}
    return {"error": "User not found."}

# Preprocess input to handle word-to-number conversion
def preprocess_input(prompt):
    words = prompt.split()
    for i, word in enumerate(words):
        try:
            words[i] = str(w2n.word_to_num(word))
        except ValueError:
            pass  # Leave unchanged if not convertible
    return " ".join(words)

# Fallback for basic calculations if LLM fails
def fallback_calculation(prompt):
    try:
        processed_prompt = preprocess_input(prompt)
        if "add" in processed_prompt or "sum" in processed_prompt:
            nums = [float(n) for n in processed_prompt.split() if n.replace('.', '', 1).isdigit()]
            return f"The sum of {nums[0]} and {nums[1]} is {add(nums[0], nums[1])}."
        elif "subtract" in processed_prompt or "difference" in processed_prompt:
            nums = [float(n) for n in processed_prompt.split() if n.replace('.', '', 1).isdigit()]
            return f"The difference between {nums[0]} and {nums[1]} is {subtract(nums[0], nums[1])}."
        elif "multiply" in processed_prompt or "product" in processed_prompt:
            nums = [float(n) for n in processed_prompt.split() if n.replace('.', '', 1).isdigit()]
            return f"The product of {nums[0]} and {nums[1]} is {multiply(nums[0], nums[1])}."
        elif "divide" in processed_prompt or "quotient" in processed_prompt:
            nums = [float(n) for n in processed_prompt.split() if n.replace('.', '', 1).isdigit()]
            result = divide(nums[0], nums[1])
            if result == "Error: Division by zero":
                return result
            return f"The result of dividing {nums[0]} by {nums[1]} is {result}."
        return "Fallback: Unable to process the calculation. Please check your input."
    except Exception as e:
        return f"Fallback Error: {e}"

# Call Groq API for LLM function calling
def call_llm(prompt):
    processed_prompt = preprocess_input(prompt)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": processed_prompt}],
        "functions": [
            {
                "name": "add",
                "description": "Adds two numbers together.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number", "description": "The first number to add."},
                        "b": {"type": "number", "description": "The second number to add."}
                    },
                    "required": ["a", "b"]
                }
            },
            {
                "name": "subtract",
                "description": "Subtracts the second number from the first.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number", "description": "The number to subtract from."},
                        "b": {"type": "number", "description": "The number to subtract."}
                    },
                    "required": ["a", "b"]
                }
            },
            {
                "name": "multiply",
                "description": "Multiplies two numbers together.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number", "description": "The first number to multiply."},
                        "b": {"type": "number", "description": "The second number to multiply."}
                    },
                    "required": ["a", "b"]
                }
            },
            {
                "name": "divide",
                "description": "Divides the first number by the second.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number", "description": "The number to divide."},
                        "b": {"type": "number", "description": "The number to divide by."}
                    },
                    "required": ["a", "b"]
                }
            }
        ]
    }

    try:
        response = requests.post(API_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        # Extract function call data
        function_calls = data.get('choices', [{}])[0].get('message', {}).get('tool_calls', [])
        if function_calls:
            function_name = function_calls[0]['function']['name']
            arguments = json.loads(function_calls[0]['function']['arguments'])
            if function_name == "add":
                return f"The sum of {arguments['a']} and {arguments['b']} is {add(arguments['a'], arguments['b'])}."
            elif function_name == "subtract":
                return f"The difference between {arguments['a']} and {arguments['b']} is {subtract(arguments['a'], arguments['b'])}."
            elif function_name == "multiply":
                return f"The product of {arguments['a']} and {arguments['b']} is {multiply(arguments['a'], arguments['b'])}."
            elif function_name == "divide":
                result = divide(arguments['a'], arguments['b'])
                if result == "Error: Division by zero":
                    return result
                return f"The result of dividing {arguments['a']} by {arguments['b']} is {result}."
        return fallback_calculation(prompt)  # Fallback to local calculation if no valid function is called
    except requests.exceptions.RequestException as e:
        return f"Error calling LLM API: {e}"

# Random joke feature
def random_joke():
    jokes = [
        "Why was the math book sad? It had too many problems!",
        "Parallel lines have so much in common. It's a shame they'll never meet.",
        "Why don't skeletons fight each other? They don't have the guts!",
        "What do you call fake spaghetti? An impasta!",
        "Why cant you hear a pterodactyl go to the bathroom? Because the p is silent!",
    ]
    return random.choice(jokes)

# Main function
def main():
    print("Welcome to the Calculator App!")
    if len(sys.argv) > 1:
        # Non-interactive mode: process command-line arguments
        command = " ".join(sys.argv[1:])
        if command.lower() == "history":
            display_history()
        elif command.startswith("user"):
            _, email = command.split(maxsplit=1)
            result = fetch_user_by_email(email)
            print(result)
        elif command.lower() == "joke":
            print(random_joke())
        else:
            result = call_llm(command)
            print(result)
            save_history(command, result)
    else:
        # Interactive mode
        print("Type 'add', 'subtract', 'multiply', or 'divide' followed by two numbers.")
        print("Or type 'user <email>' to fetch user details, 'history' to view calculations, 'joke' for a joke, or 'exit' to quit.")
        try:
            while True:
                command = input("> ").strip()
                if command.lower() == "exit":
                    print("Goodbye!")
                    break
                elif command.lower() == "history":
                    display_history()
                elif command.startswith("user"):
                    _, email = command.split(maxsplit=1)
                    result = fetch_user_by_email(email)
                    print(result)
                elif command.lower() == "joke":
                    print(random_joke())
                else:
                    result = call_llm(command)
                    print(result)
                    save_history(command, result)
        except EOFError:
            print("EOF detected. Running in non-interactive mode. Exiting gracefully.")

if __name__ == "__main__":
    main()

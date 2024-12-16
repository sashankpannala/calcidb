# CalciDB

**CalciDB** is a Python-powered calculator application enhanced with **LLM function calling** and persistent history tracking using **SQLite**. It supports natural language arithmetic operations and allows seamless interaction via the command line or Docker.

---

## Features

- **LLM-Powered Calculations**:
  - Dynamically processes arithmetic operations via LLM APIs.
  - Supports natural language inputs like: `What is 10 plus 20?`.

- **Persistent Calculation History**:
  - Saves all user calculations and results to a SQLite database.
  - Allows users to view their calculation history interactively.

- **User Management**:
  - Seeds the database with sample user data for testing.

- **Docker Integration**:
  - Simplifies setup and deployment using Docker and Docker Compose.

---

## Requirements

- Python 3.8 or above
- SQLite
- Docker (optional)

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/sashankpannala/calcidb.git
cd calcidb


2. Create a Virtual Environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Set Up Environment Variables
Create a .env file in the project root with the following content:
API_KEY=<your_llm_api_key>
Replace <your_llm_api_key> with the actual API key for the LLM service.


Here is a professional and polished README.md file for your project:

markdown
Copy code
# CalciDB

**CalciDB** is a Python-powered calculator application enhanced with **LLM function calling** and persistent history tracking using **SQLite**. It supports natural language arithmetic operations and allows seamless interaction via the command line or Docker.

---

## Features

- **LLM-Powered Calculations**:
  - Dynamically processes arithmetic operations via LLM APIs.
  - Supports natural language inputs like: `What is 10 plus 20?`.

- **Persistent Calculation History**:
  - Saves all user calculations and results to a SQLite database.
  - Allows users to view their calculation history interactively.

- **User Management**:
  - Seeds the database with sample user data for testing.

- **Docker Integration**:
  - Simplifies setup and deployment using Docker and Docker Compose.

---

## Requirements

- Python 3.8 or above
- SQLite
- Docker (optional)

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/sashankpannala/calcidb.git
cd calcidb
2. Create a Virtual Environment
bash
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
4. Set Up Environment Variables
Create a .env file in the project root with the following content:

env
Copy code
API_KEY=<your_llm_api_key>
Replace <your_llm_api_key> with the actual API key for the LLM service.

Usage
Run the Application
python main.py

Run with Docker
Build the Docker Image
docker build -t calcidb .
Run the Application in a Container

Interactive Mode:
docker run -it calcidb
Environment Variable Input:
docker run -e CALC_PROMPT="Add 10 and 20" calcidb

Testing
Run Unit Tests
This project includes unit tests for:
Arithmetic functions
LLM function calls
Database history
To run the tests:
pytest

Expected output:

================================================= test session starts =================================================
platform linux -- Python 3.10.12, pytest-8.3.3
collected 6 items                                                                                                     

test_main.py ......                                                                                                   [100%]

================================================== 6 passed in 0.45s ==================================================

Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request for new features, improvements, or bug fixes.

License
This project is licensed under the MIT License. See the LICENSE file for more details.

Author
Created by Sai Sashank Pannala.




CalciDB is a Python-based calculator application powered by LLM function calling and SQLite for database integration. It supports basic arithmetic operations, tracks persistent calculation history, and allows for seamless interaction through the command line or Docker.

Features
LLM-Powered Calculations: Uses LLM API calls to dynamically process arithmetic operations. Supports flexible natural language input (e.g., "What is the sum of 5 and 3?").
Persistent Calculation History: Saves all calculations and their results to a SQLite database (calculation_history table). Allows users to view the history interactively.
User Management: Seeds the database with sample user data.
Docker Support: Easy setup and deployment using Docker and Docker Compose.
Requirements
Python 3.8+
SQLite
Docker (optional)
Setup Instructions
1. Clone the Repository
bash
Copy code
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
bash
Copy code
python main.py  
Interactive Mode Commands
Perform a Calculation: Enter natural language instructions like:

sql
Copy code
Add 5 and 3  
Expected output:

python
Copy code
Result: The sum of 5 and 3 is 8.  
View Calculation History: Enter history to display all saved calculations.

python
Copy code
Calculation History:  
1. Add 5 and 3 -> The sum of 5 and 3 is 8.  
Exit the Application: Enter exit.

Run with Docker
Build the Docker Image
bash
Copy code
docker build -t calcidb .  
Run the Application in a Container
Interactive Mode:

bash
Copy code
docker run -it calcidb  
Environment Variable Input:

bash
Copy code
docker run -e CALC_PROMPT="Add 10 and 20" calcidb  
Database Structure
Users Table (users)
Column Name	Data Type	Description
id	Integer	Primary key
first_name	String	User's first name
last_name	String	User's last name
email	String	Unique email
username	String	Unique username
Calculation History Table (calculation_history)
Column Name	Data Type	Description
id	Integer	Primary key
calculation	String	User input (e.g., "Add 5 and 3")
result	String	Result of the calculation
Testing
Run Unit Tests
This project includes unit tests for the arithmetic functions, LLM function calls, and database history.

bash
Copy code
pytest  
Expected output:

plaintext
Copy code
=========================testsessionstarts=================================================  
platform linux -- Python 3.10.12, pytest-8.3.3  collected    6items                                                                                                       
test_main.py ......                                                                                                   [100%]  
================================================== 6 passed in 0.45s =================================================  
Contributing
Contributions are welcome! Please create a pull request or open an issue for any feature requests or bug reports.

License
This project is licensed under the MIT License. See the LICENSE file for details.

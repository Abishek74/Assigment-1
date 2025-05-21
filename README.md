**Insurance Claims Management App**


This is a simple insurance data management and analysis app built with Python and Streamlit.
It allows users to register policyholders, add and track claims, analyze risk, and view reports with interactive charts.

Register policyholders with policy details

Add and manage insurance claims

Automatically flag high-risk policyholders

View interactive reports:

Bar chart: Policy registrations per month

Line chart: Claims per month

Metric cards: Average claim per policy type

Filter reports by policy type

*** To Run App ****

# Step 1: Clone the repository
git clone https://github.com/Abishek74/Assigment-1.git

# Step 2: Navigate into the project directory
cd Assigment-1/Insurance_app

# Step 3: Create a virtual environment
python -m venv vn

# Step 4: Activate the virtual environment
vn\Scripts\activate   # On Windows
# source vn/bin/activate   # On macOS/Linux

# Step 5: Install dependencies
pip install -r requirements.txt

# Step 6: Run the Streamlit app
streamlit run app.py

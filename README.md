# Placement-Eligibility-App
A Streamlit-based web application to help filter students eligible for campus placements based on their CGPA, programming skills, and soft skills.

# Features
i. Student eligibility checking based on criteria:
      -Minimum CGPA
      -Minimum programming problems solved
      -Minimum soft skills average score
ii. Interactive web interface built with Streamlit
iii. Real-time query from SQLite database
iv. User-friendly dashboard to view eligible students

# Tech Stack
Python 3.7
Streamlit
SQLite
Pandas

# Setup Instructions
1️⃣ Clone this repo
git clone https://github.com/yourusername/PlacementApp.git
cd PlacementApp

2️⃣ Create a virtual environment (recommended)
python -m venv env
source env/bin/activate   # For Linux/Mac
env\Scripts\activate      # For Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the Streamlit app
streamlit run streamlit_app.py

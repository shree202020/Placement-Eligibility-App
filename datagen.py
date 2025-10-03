import sqlite3
import random
import os

# ---------------------------
# Remove old DB if exists
# ---------------------------
DB_FILE = "placement.db"
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

# ---------------------------
# Connect to SQLite
# ---------------------------
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()

# ---------------------------
# Create Tables
# ---------------------------
c.execute('''CREATE TABLE students(
    student_id INTEGER PRIMARY KEY,
    name TEXT,
    branch TEXT,
    cgpa REAL,
    gender TEXT,
    email TEXT,
    phone TEXT,
    city TEXT,
    tenth REAL,
    twelfth REAL
)''')

c.execute('''CREATE TABLE programming(
    student_id INTEGER,
    c INTEGER,
    cpp INTEGER,
    java INTEGER,
    python INTEGER,
    ds INTEGER,
    algo INTEGER,
    FOREIGN KEY(student_id) REFERENCES students(student_id)
)''')

c.execute('''CREATE TABLE soft_skills(
    student_id INTEGER,
    comm INTEGER,
    team INTEGER,
    leadership INTEGER,
    creativity INTEGER,
    adaptability INTEGER,
    time_mgmt INTEGER,
    FOREIGN KEY(student_id) REFERENCES students(student_id)
)''')

c.execute('''CREATE TABLE placements(
    student_id INTEGER,
    company TEXT,
    role TEXT,
    package REAL,
    location TEXT,
    round1 INTEGER,
    round2 INTEGER,
    round3 INTEGER,
    selected INTEGER,
    FOREIGN KEY(student_id) REFERENCES students(student_id)
)''')

# ---------------------------
# Data Generators
# ---------------------------
branches = ["CSE", "ECE", "EEE", "MECH", "CIVIL"]
cities = ["Chennai", "Bangalore", "Hyderabad", "Delhi", "Mumbai"]
companies = ["TCS", "Infosys", "Wipro", "HCL", "Cognizant", "Accenture"]

def generate_student(sid):
    name = f"Student{sid}"
    branch = random.choice(branches)
    cgpa = round(random.uniform(5.0, 10.0), 2)
    gender = random.choice(["Male", "Female"])
    email = f"student{sid}@example.com"
    phone = f"9{random.randint(100000000, 999999999)}"
    city = random.choice(cities)
    tenth = round(random.uniform(60, 100), 2)
    twelfth = round(random.uniform(60, 100), 2)
    return (sid, name, branch, cgpa, gender, email, phone, city, tenth, twelfth)

def generate_programming(sid):
    return (
        sid,
        random.randint(1, 10),  # C
        random.randint(1, 10),  # C++
        random.randint(1, 10),  # Java
        random.randint(1, 10),  # Python
        random.randint(1, 10),  # DS
        random.randint(1, 10)   # Algo
    )

def generate_softskills(sid):
    return (
        sid,
        random.randint(1, 10),  # Communication
        random.randint(1, 10),  # Teamwork
        random.randint(1, 10),  # Leadership
        random.randint(1, 10),  # Creativity
        random.randint(1, 10),  # Adaptability
        random.randint(1, 10)   # Time Management
    )

def generate_placement(sid):
    company = random.choice(companies)
    role = random.choice(["Software Engineer", "Analyst", "Developer", "Tester"])
    package = round(random.uniform(3.0, 12.0), 2)
    location = random.choice(cities)
    r1, r2, r3 = [random.randint(0, 1) for _ in range(3)]
    selected = 1 if (r1 and r2 and r3) else 0
    return (sid, company, role, package, location, r1, r2, r3, selected)

# ---------------------------
# Populate Database
# ---------------------------
def populate_db(num_students=500):
    for sid in range(1, num_students + 1):
        student = generate_student(sid)
        c.execute("INSERT INTO students VALUES (?,?,?,?,?,?,?,?,?,?)", student)

        prog = generate_programming(sid)
        c.execute("INSERT INTO programming VALUES (?,?,?,?,?,?,?)", prog)

        soft = generate_softskills(sid)
        c.execute("INSERT INTO soft_skills VALUES (?,?,?,?,?,?,?)", soft)

        place = generate_placement(sid)
        c.execute("INSERT INTO placements VALUES (?,?,?,?,?,?,?,?,?)", place)

    conn.commit()
    print(f"Database populated with {num_students} students.")

# ---------------------------
# Main
# ---------------------------
if __name__ == "__main__":
    populate_db(500)
    conn.close()

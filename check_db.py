import sqlite3

# Connect to database
conn = sqlite3.connect("placement.db")
c = conn.cursor()

print("\nFirst 5 students:")
for row in c.execute("SELECT * FROM students LIMIT 5"):
    print(row)

print("\nFirst 5 programming skills:")
for row in c.execute("SELECT * FROM programming LIMIT 5"):
    print(row)

print("\nFirst 5 placements:")
for row in c.execute("SELECT * FROM placements LIMIT 5"):
    print(row)

conn.close()

import mysql.connector

with open("init_db.sql") as f:
    sql = f.read()

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root"
)

cursor = conn.cursor()
for statement in sql.split(";"):
    if statement.strip():
        print(statement)
        cursor.execute(statement)
        conn.commit()
        print("Statement executed")

cursor.close()
conn.close()

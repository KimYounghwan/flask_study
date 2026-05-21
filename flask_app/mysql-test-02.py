import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="school"
)

# ===== 기본 커서 (튜플) =====
cursor = conn.cursor()
cursor.execute("SELECT student_id, name, age FROM students where student_id=1")
result = cursor.fetchone()

print(result)           # (1, '김철수', 25)
print(result[0])        # 1      ← 인덱스로 접근 (0부터)
print(result[1])        # '김철수'
print(result[2])        # 25

cursor.close()

# ===== 딕셔너리 커서 =====
cursor_dict = conn.cursor(dictionary=True)
cursor_dict.execute("SELECT student_id, name, age FROM students where student_id=1")
result_dict = cursor_dict.fetchone()

print(result_dict)      # {'student_id': 1, 'name': '김철수', 'age': 25}
print(result_dict['student_id'])  # 1      ← 이름으로 접근!
print(result_dict['name'])        # '김철수'
print(result_dict['age'])         # 25

cursor_dict.close()
conn.close()
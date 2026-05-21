import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="school",
    autocommit=True
)
cursor = conn.cursor()

# ===== SELECT 실행 =====
# cursor.execute("SELECT * FROM students")

# ===== INSERT 실행 =====
# (10, '전지현', 26, 'F', '2000-06-25', 89.00);

# cursor.execute(
#     "INSERT INTO students " +
#     "(student_id, name, age, gender) " +
#     "VALUES (%s,%s,%s,%s)",
#     (11, '고윤정', 30, 'F')
# )

# # ===== UPDATE 실행 =====
# cursor.execute(
#     "UPDATE students SET age = %s WHERE name = %s",
#     (31,'고윤정')
# )
# print('UPDATE 실행')

# # ===== DELETE 실행 =====
# 고윤정 삭제하기
cursor.execute(
    "DELETE FROM students WHERE name = %s",
    ('고윤정',)
)
print('DELETE 실행')

cursor.close()
conn.close()
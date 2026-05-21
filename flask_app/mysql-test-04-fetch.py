# mysql-test-03.py의 맨앞 10줄 북붙
import mysql.connector 

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="school",
    autocommit=True
)
cursor = conn.cursor()

# 결과가 없는 경우
cursor.execute("SELECT * FROM students WHERE age > 100")
results = cursor.fetchall()

print(results)          # []  ← 빈 리스트
print(len(results))     # 0

# 안전하게 처리
if not results:         # 빈 리스트는 False
    print("데이터가 없습니다!")
else:
    for row in results:
        print(row)

# 또는
if len(results) == 0:
    print("데이터가 없습니다!")

# mysql-test-03.py의 맨뒤 2줄 북붙
cursor.close()
conn.close()    
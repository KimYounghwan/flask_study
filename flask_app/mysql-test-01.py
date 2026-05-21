# ① 라이브러리 불러오기
import mysql.connector

# ② DB 연결 (Connection 객체 생성)
conn = mysql.connector.connect(
    host="localhost",      # 서버 주소 (내 컴퓨터 = localhost)
    user="root",           # 사용자 이름
    password="1234",  # 비밀번호
    database="school"     # 사용할 데이터베이스 이름
)

# ③ 커서 생성 (Cursor 객체)
cursor = conn.cursor()

# ④ SQL 실행
cursor.execute("SELECT * FROM students")

# ⑤ 결과 가져오기
results = cursor.fetchall()
print(results)

# ⑥ 자원 정리 (반드시 해야 함!)
cursor.close()   # 커서 닫기
conn.close()     # 연결 닫기
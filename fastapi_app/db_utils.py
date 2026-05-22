# db_utils.py - 데이터베이스 조작 함수들

import mysql.connector
from mysql.connector import Error
from db_config import DB_CONFIG

def get_connection():
    """DB 연결을 생성하는 함수"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"DB 연결 실패: {e}")
        return None

# ===== CREATE (생성) =====
def create_student(name, age, gender):
    """
    새 학생을 추가하는 함수
    입력: name(이름), age(나이), gender(성별)
    반환: 추가된 학생의 ID 또는 None
    """
    conn = get_connection()
    if not conn:
        return None

    cursor = conn.cursor()

    try:
        sql = "INSERT INTO students (name, age, gender) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, age, gender))
        conn.commit()

        new_id = cursor.lastrowid  # ← 방금 추가된 ID
        print(f"학생 추가 성공! ID: {new_id}")
        return new_id

    except Error as e:
        print(f"추가 실패: {e}")
        conn.rollback()
        return None

    finally:
        cursor.close()
        conn.close()

# ===== READ (조회) =====
def get_all_students():
    """
    모든 학생을 조회하는 함수
    반환: 학생 목록 (딕셔너리 리스트) 또는 None
    """
    conn = get_connection()
    if not conn:
        return None

    cursor = conn.cursor(dictionary=True)

    try:
        sql = "SELECT * FROM students"
        cursor.execute(sql)
        results = cursor.fetchall()
        return results

    except Error as e:
        print(f"조회 실패: {e}")
        return None

    finally:
        cursor.close()
        conn.close()

def get_student_by_id(student_id):
    """
    특정 ID의 학생을 조회하는 함수
    입력: student_id (학생 번호)
    반환: 학생 정보 (딕셔너리) 또는 None
    """
    conn = get_connection()
    if not conn:
        return None

    cursor = conn.cursor(dictionary=True)

    try:
        sql = "SELECT * FROM students WHERE student_id = %s"
        cursor.execute(sql, (student_id,))
        result = cursor.fetchone()  # ← 한 명만!
        return result

    except Error as e:
        print(f"조회 실패: {e}")
        return None

    finally:
        cursor.close()
        conn.close()

# ===== UPDATE (수정) =====
def update_student(student_id, name=None, age=None, gender=None):
    """
    학생 정보를 수정하는 함수
    입력: student_id (필수), 수정할 항목들 (선택)
    반환: 성공 여부 (True/False)
    """
    conn = get_connection()
    if not conn:
        return False

    cursor = conn.cursor()

    try:
        # 동적 SQL 생성 (수정할 항목만 포함)
        updates = []
        params = []

        if name is not None:
            updates.append("name = %s")
            params.append(name)
        if age is not None:
            updates.append("age = %s")
            params.append(age)
        if gender is not None:
            updates.append("gender = %s")
            params.append(gender)

        if not updates:
            print("수정할 내용이 없습니다.")
            return False

        params.append(student_id)  # WHERE 조건용

        sql = f"UPDATE students SET {', '.join(updates)} WHERE student_id = %s"
        cursor.execute(sql, tuple(params))
        conn.commit()

        if cursor.rowcount > 0:
            print(f"학생 {student_id} 수정 성공!")
            return True
        else:
            print(f"학생 {student_id}을 찾을 수 없습니다.")
            return False

    except Error as e:
        print(f"수정 실패: {e}")
        conn.rollback()
        return False

    finally:
        cursor.close()
        conn.close()

# ===== DELETE (삭제) =====
def delete_student(student_id):
    """
    학생을 삭제하는 함수
    입력: student_id (학생 번호)
    반환: 성공 여부 (True/False)
    """
    conn = get_connection()
    if not conn:
        return False

    cursor = conn.cursor()

    try:
        sql = "DELETE FROM students WHERE student_id = %s"
        cursor.execute(sql, (student_id,))
        conn.commit()

        if cursor.rowcount > 0:
            print(f"학생 {student_id} 삭제 성공!")
            return True
        else:
            print(f"학생 {student_id}을 찾을 수 없습니다.")
            return False

    except Error as e:
        print(f"삭제 실패: {e}")
        conn.rollback()
        return False

    finally:
        cursor.close()
        conn.close()
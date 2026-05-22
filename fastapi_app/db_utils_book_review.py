# db_utils_review.py - 독후감 테이블 처리 함수들

import mysql.connector
from mysql.connector import Error
from db_config_book import DB_CONFIG


def get_connection():
    """DB 연결 생성"""

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn

    except Error as e:
        print(f"DB 연결 실패: {e}")
        return None


# =====================================================
# CREATE (독후감 추가)
# =====================================================
def create_review(book_id, content):
    """
    독후감을 추가하는 함수

    입력:
        book_id, content

    반환:
        추가된 독후감 ID 또는 None
    """

    conn = get_connection()

    if not conn:
        return None

    cursor = conn.cursor()

    try:

        sql = """
        INSERT INTO book_reviews
        (book_id, content)
        VALUES (%s, %s)
        """

        values = (
            book_id,
            content
        )

        cursor.execute(sql, values)

        conn.commit()

        new_id = cursor.lastrowid

        print(f"독후감 추가 성공! ID: {new_id}")

        return new_id

    except Error as e:
        print(f"독후감 추가 실패: {e}")

        conn.rollback()

        return None

    finally:
        cursor.close()
        conn.close()


# =====================================================
# READ (전체 조회)
# =====================================================
def get_all_reviews():
    """
    모든 독후감을 조회하는 함수

    반환:
        독후감 목록(dict 리스트)
    """

    conn = get_connection()

    if not conn:
        return None

    cursor = conn.cursor(dictionary=True)

    try:

        sql = """
        SELECT
            r.review_id,
            r.book_id,
            r.content,
            r.created_at,
            b.title
        FROM book_reviews r
        JOIN books b
            ON r.book_id = b.book_id
        ORDER BY r.review_id DESC
        """

        cursor.execute(sql)

        results = cursor.fetchall()

        return results

    except Error as e:
        print(f"조회 실패: {e}")

        return None

    finally:
        cursor.close()
        conn.close()


# =====================================================
# READ (ID 조회)
# =====================================================
def get_review_by_id(review_id):
    """
    특정 독후감을 조회하는 함수

    입력:
        review_id

    반환:
        독후감 정보(dict) 또는 None
    """

    conn = get_connection()

    if not conn:
        return None

    cursor = conn.cursor(dictionary=True)

    try:

        sql = """
        SELECT
            r.review_id,
            r.book_id,
            r.content,
            r.created_at,
            b.title
        FROM book_reviews r
        JOIN books b
            ON r.book_id = b.book_id
        WHERE r.review_id = %s
        """

        cursor.execute(sql, (review_id,))

        result = cursor.fetchone()

        return result

    except Error as e:
        print(f"조회 실패: {e}")

        return None

    finally:
        cursor.close()
        conn.close()


# =====================================================
# UPDATE (수정)
# =====================================================
def update_review(review_id, book_id=None, content=None):
    """
    독후감을 수정하는 함수

    반환:
        성공 여부(True / False)
    """

    conn = get_connection()

    if not conn:
        return False

    cursor = conn.cursor()

    try:

        updates = []
        params = []

        if book_id is not None:
            updates.append("book_id = %s")
            params.append(book_id)

        if content is not None:
            updates.append("content = %s")
            params.append(content)

        if not updates:
            print("수정할 내용이 없습니다.")
            return False

        params.append(review_id)

        sql = f"""
        UPDATE book_reviews
        SET {', '.join(updates)}
        WHERE review_id = %s
        """

        cursor.execute(sql, tuple(params))

        conn.commit()

        if cursor.rowcount > 0:
            print(f"독후감 {review_id} 수정 성공!")
            return True

        else:
            print(f"독후감 {review_id}를 찾을 수 없습니다.")
            return False

    except Error as e:
        print(f"수정 실패: {e}")

        conn.rollback()

        return False

    finally:
        cursor.close()
        conn.close()


# =====================================================
# DELETE (삭제)
# =====================================================
def delete_review(review_id):
    """
    독후감을 삭제하는 함수

    입력:
        review_id

    반환:
        성공 여부(True / False)
    """

    conn = get_connection()

    if not conn:
        return False

    cursor = conn.cursor()

    try:

        sql = "DELETE FROM book_reviews WHERE review_id = %s"

        cursor.execute(sql, (review_id,))

        conn.commit()

        if cursor.rowcount > 0:
            print(f"독후감 {review_id} 삭제 성공!")
            return True

        else:
            print(f"독후감 {review_id}를 찾을 수 없습니다.")
            return False

    except Error as e:
        print(f"삭제 실패: {e}")

        conn.rollback()

        return False

    finally:
        cursor.close()
        conn.close()


# =====================================================
# COUNT (행 개수)
# =====================================================
def count_review():
    """
    book_reviews 테이블의 전체 행 개수를 반환하는 함수

    반환:
        행 개수(int) 또는 None
    """

    conn = get_connection()

    if not conn:
        return None

    cursor = conn.cursor()

    try:

        sql = "SELECT COUNT(*) FROM book_reviews"

        cursor.execute(sql)

        result = cursor.fetchone()

        count = result[0]

        return count

    except Error as e:
        print(f"개수 조회 실패: {e}")

        return None

    finally:
        cursor.close()
        conn.close()
# db_utils_book.py - 도서 테이블 처리 함수들

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
# CREATE (도서 추가)
# =====================================================
def create_book(isbn, title, author, publisher, publish_date, price):
    """
    새 도서를 추가하는 함수

    입력:
        isbn, title, author, publisher,
        publish_date, price

    반환:
        추가된 도서 ID 또는 None
    """

    conn = get_connection()

    if not conn:
        return None

    cursor = conn.cursor()

    try:
        sql = """
        INSERT INTO books
        (isbn, title, author, publisher, publish_date, price)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            isbn,
            title,
            author,
            publisher,
            publish_date,
            price
        )

        cursor.execute(sql, values)

        conn.commit()

        new_id = cursor.lastrowid

        print(f"도서 추가 성공! ID: {new_id}")

        return new_id

    except Error as e:
        print(f"도서 추가 실패: {e}")

        conn.rollback()

        return None

    finally:
        cursor.close()
        conn.close()


# =====================================================
# READ (전체 조회)
# =====================================================
def get_all_books():
    """
    모든 도서를 조회하는 함수

    반환:
        도서 목록(dict 리스트)
    """

    conn = get_connection()

    if not conn:
        return None

    cursor = conn.cursor(dictionary=True)

    try:
        sql = "SELECT * FROM books ORDER BY title"

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
def get_book_by_id(book_id):
    """
    특정 도서를 조회하는 함수

    입력:
        book_id

    반환:
        도서 정보(dict) 또는 None
    """

    conn = get_connection()

    if not conn:
        return None

    cursor = conn.cursor(dictionary=True)

    try:
        sql = "SELECT * FROM books WHERE book_id = %s"

        cursor.execute(sql, (book_id,))

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
def update_book(
    book_id,
    isbn=None,
    title=None,
    author=None,
    publisher=None,
    publish_date=None,
    price=None
):
    """
    도서 정보를 수정하는 함수

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

        if isbn is not None:
            updates.append("isbn = %s")
            params.append(isbn)

        if title is not None:
            updates.append("title = %s")
            params.append(title)

        if author is not None:
            updates.append("author = %s")
            params.append(author)

        if publisher is not None:
            updates.append("publisher = %s")
            params.append(publisher)

        if publish_date is not None:
            updates.append("publish_date = %s")
            params.append(publish_date)

        if price is not None:
            updates.append("price = %s")
            params.append(price)

        if not updates:
            print("수정할 내용이 없습니다.")
            return False

        params.append(book_id)

        sql = f"""
        UPDATE books
        SET {', '.join(updates)}
        WHERE book_id = %s
        """

        cursor.execute(sql, tuple(params))

        conn.commit()

        if cursor.rowcount > 0:
            print(f"도서 {book_id} 수정 성공!")
            return True

        else:
            print(f"도서 {book_id}를 찾을 수 없습니다.")
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
def delete_book(book_id):
    """
    도서를 삭제하는 함수

    입력:
        book_id

    반환:
        성공 여부(True / False)
    """

    conn = get_connection()

    if not conn:
        return False

    cursor = conn.cursor()

    try:
        sql = "DELETE FROM books WHERE book_id = %s"

        cursor.execute(sql, (book_id,))

        conn.commit()

        if cursor.rowcount > 0:
            print(f"도서 {book_id} 삭제 성공!")
            return True

        else:
            print(f"도서 {book_id}를 찾을 수 없습니다.")
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
def count_book():
    """
    books 테이블의 전체 행 개수를 반환하는 함수

    반환:
        행 개수(int) 또는 None
    """

    conn = get_connection()

    if not conn:
        return None

    cursor = conn.cursor()

    try:
        sql = "SELECT COUNT(*) FROM books"

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
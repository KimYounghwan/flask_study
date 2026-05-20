from flask import Flask, render_template, request
import db_utils_book as bookdb
import db_utils_book_review as book_reviewdb

app = Flask(__name__)
"""
** 기능별 URL 정의 ***
*도서등록 - /book/insert GET->폼, POST-> action  ( book/insert_form, book/insert_action )
*도서목록 - /book/list
*도서상세 - /book/detail/<book_id>
*도서수정 - /book/update/<book_id>
*도서삭제 - /book/delete/<book_id>
"""
# ============================================
# 독후감 삭제
# URL: /book_review/delete/<review_id>
# POST -> 삭제 처리
# ============================================
@app.route("/book_review/delete/<review_id>", methods=['POST'])
def book_review_delete(review_id):
    """
    독후감 삭제 처리
    - review_id로 독후감 삭제
    - 삭제 후 독후감 목록으로 이동
    """
    # DB 삭제
    result = book_reviewdb.delete_review(review_id)

    # 삭제 실패
    if result == False:
        return render_template(
            "book/result.html",
            title="독후감 삭제 실패",
            msg="독후감 삭제에 실패했습니다",
            link="/book_review/list",
            link_text="독후감목록")

    # 삭제 성공
    return render_template(
        "book/result.html",
        title="독후감 삭제 성공",
        msg="독후감을 성공적으로 삭제했습니다",
        link="/book_review/list",
        link_text="독후감목록")
# ============================================
# 독후감 수정
# URL: /book_review/update/<review_id>
# GET -> 수정 폼, POST -> 수정 처리
# ============================================
@app.route("/book_review/update/<review_id>", methods=['GET', 'POST'])
def book_review_update(review_id):
    """
    독후감 수정 페이지
    GET: 수정 폼 보여주기 (도서목록 + 기존 독후감 내용)
    POST: 수정 처리
    """
    # GET 요청 - 수정 폼
    if request.method == "GET":
        # 기존 독후감 정보 조회
        review = book_reviewdb.get_review_by_id(review_id)

        # 독후감이 없는 경우
        if review == None:
            return render_template(
                "book/result.html",
                title="독후감 검색 오류",
                msg="없거나 삭제된 독후감입니다",
                link="/book_review/list",
                link_text="독후감목록")

        # 도서 목록 조회 (select option용)
        book_list = bookdb.get_all_books()

        # 수정 폼 렌더링
        return render_template(
            "book_review/update_form.html",
            review=review,
            book_list=book_list)

    # POST 요청 - 수정 처리
    if request.method == "POST":
        # 폼 데이터 받기
        review_id = request.form.get("review_id")
        book_id = request.form.get("book_id")
        content = request.form.get("content")

        # DB 수정
        result = book_reviewdb.update_review(
            review_id=review_id,
            book_id=book_id,
            content=content)

        # 수정 실패
        if result == False:
            return render_template(
                "book/result.html",
                title="독후감 수정 실패",
                msg="독후감 수정에 실패했습니다",
                link="/book_review/list",
                link_text="독후감목록")

        # 수정 성공
        return render_template(
            "book/result.html",
            title="독후감 수정 성공",
            msg="독후감을 성공적으로 수정했습니다",
            link="/book_review/detail/" + review_id,
            link_text="수정된 독후감 보기")

# ============================================
# 독후감 상세보기
# ============================================
@app.route("/book_review/detail/<review_id>")
def book_review_detail(review_id):
    """
    독후감 상세 페이지
    - review_id로 독후감 정보 조회
    - 해당 독후감의 도서 정보도 함께 조회
    """
    # 독후감 정보 조회 (JOIN으로 도서제목도 포함)
    review = book_reviewdb.get_review_by_id(review_id)
    
    # 독후감이 없는 경우
    if review == None:
        return render_template(
            "book/result.html",
            title="독후감 검색 오류",
            msg="없거나 삭제된 독후감입니다",
            link="/book_review/list",
            link_text="독후감목록")
    
    # 해당 독후감의 도서 정보 조회
    book = bookdb.get_book_by_id(review["book_id"])
    
    # 도서 정보가 없는 경우
    if book == None:
        return render_template(
            "book/result.html",
            title="도서 검색 오류",
            msg="해당 도서 정보를 찾을 수 없습니다",
            link="/book_review/list",
            link_text="독후감목록")
    
    # 독후감 상세 페이지 렌더링
    return render_template(
        "book_review/detail.html",
        review=review,
        book=book)

# 독후감등록
@app.route("/book_review/insert",methods=['GET','POST'])
def book_review_insert():
    if request.method == "GET":
        book_list = bookdb.get_all_books()
        return render_template("book_review/insert_form.html",book_list=book_list)
    if request.method == "POST":
        book_id = request.form.get("book_id")
        content = request.form.get("content")
    book_reviewdb.create_review(book_id,content)
    return render_template(
        "book/result.html", 
        title="독후감등록성공",
        msg="독후감 등록을 성공했습니다",
        link="/book_review/list",
        link_text="독후감목록")


#독후감목록
@app.route("/book_review/list")
def book_review_list():
    book_review_list = book_reviewdb.get_all_reviews()
    return render_template(
        "book_review/list.html",
        book_review_list=book_review_list
    )




# 도서삭제
@app.route("/book/delete/<book_id>")
def book_delete(book_id):
    book = bookdb.delete_book(book_id)
    if book == False:
        return render_template(
            "book/result.html", 
            title="도서검색 오류",
            msg="없거나 삭제된 도서입니다",
            link="/book/list",
            link_text="도서목록")
    return render_template(
            "book/result.html", 
            title="도서삭제",
            msg="도서를 성공적으로 삭제했습니다",
            link="/book/list",
            link_text="도서목록")

# 도서수정
@app.route("/book/update/<book_id>",methods=['GET','POST'])
def book_update(book_id):
    if request.method == "GET":
        book = bookdb.get_book_by_id(book_id)
        if book == None:
            return render_template(
                "book/result.html", 
                title="도서검색 오류",
                msg="없거나 삭제된 도서입니다",
                link="/book/list",
                link_text="도서목록")
        return render_template("book/update_form.html", book=book)
    if request.method == "POST":
        book_id = request.form.get("book_id")
        isbn = request.form.get("isbn")
        title = request.form.get("title")
        author = request.form.get("author")
        publisher = request.form.get("publisher")
        publish_date = request.form.get("publish_date")
        price = request.form.get("price")
    bookdb.update_book(book_id,isbn, title, author, publisher,publish_date,price)
    return render_template(
        "book/result.html", 
        title="책수정성공",
        msg="책정보 수정을 성공했습니다",
        link="/book/list",
        link_text="도서목록")


# 도서상세
@app.route("/book/detail/<book_id>")
def book_detail(book_id):
    book = bookdb.get_book_by_id(book_id)
    if book == None:
        return render_template(
            "book/result.html", 
            title="도서검색 오류",
            msg="없거나 삭제된 도서입니다",
            link="/book/list",
            link_text="도서목록")
    return render_template("book/detail.html", book=book)

# 메인
@app.route("/")
def review_main():
    count_book = bookdb.count_book()
    return render_template(
        "book_review_main/index.html",
        count_book=count_book)

# 도서등록
@app.route("/book/insert",methods=['GET','POST'])
def book_insert():
    if request.method == "GET":
        return render_template("book/insert_form.html")
    if request.method == "POST":
        isbn = request.form.get("isbn")
        title = request.form.get("title")
        author = request.form.get("author")
        publisher = request.form.get("publisher")
        publish_date = request.form.get("publish_date")
        price = request.form.get("price")
    bookdb.create_book(isbn, title, author, publisher,publish_date,price)
    return render_template(
        "book/result.html", 
        title="책등록성공",
        msg="책정보 등록을 성공했습니다",
        link="/book/list",
        link_text="도서목록")

#도서목록
@app.route("/book/list")
def book_list():
    book_list = bookdb.get_all_books()
    return render_template(
        "book/list.html",
        book_list=book_list
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True,)
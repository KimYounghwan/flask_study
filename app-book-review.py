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
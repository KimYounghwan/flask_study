from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import db_utils_book as bookdb
import db_utils_book_review as reviewdb

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용 (개발용)
    allow_methods=["*"],  # 모든 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# book count
@app.get("/book_count")
def book_count():
    res = bookdb.count_book()
    if res :
        return {"code":0, "count":res}
    return {"code":1, "message":"book_count Error"}

# review count
@app.get("/review_count")
def review_count():
    res = reviewdb.count_review()
    if res :
        return {"code":0, "count":res}
    return {"code":1, "message":"review_count Error"}




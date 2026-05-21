from flask import Flask, request, make_response
app = Flask(__name__)

# 쿠키 정의
@app.route("/set_cookie")
def set_cookie():
    response = make_response("쿠키설정")
    response.set_cookie("username","hong")
    return response

# 쿠키추출
@app.route("/get_cookie")
def get_cookie():
    username = request.cookies.get("username")
    return f"username = {username}"

# 쿠키 삭제
@app.route("/remove_cookie")
def remove_cookie():
    response = make_response("쿠키 삭제")
    response.delete_cookie("username")
    return response

# count 올리기
@app.route("/increase")
def increase():
    count = request.cookies.get("count")
    if count == None: #쿠키에 count없으면
        count = 0
    else: # 있으면
        count = int(count) #숫자로 변환
    count += 1 # 1증가
    res = make_response(f"count = {count}")
    res.set_cookie("count",str(count), 60*5)
    return res

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
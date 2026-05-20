# 세션 테스트
from flask import Flask, request, make_response, session
app = Flask(__name__)

app.secret_key = "abcd1234"

@app.route("/get_session")
def get_session():
    count = session.get("count")
    return f"count = {count}"

@app.route("/increase")
def increase():
    count = session.get("count",0)
    count += 1
    session["count"] = count
    return f"count = {count}"

# 로그인했을때. session["mid"] 에 회원id를 가지고 있음
# 내정보 출력
@app.route("/my_info")
def my_info():
    mid = session.get("mid")
    if mid == None:
        return f"로그인이 필요합니다. /login_form 접속하세요"
    return f"""
        회원id = {mid}
        <a href='/logout'>로그아웃</a> <br>
        """

# 로그인폼 출력
@app.route("/login_form")
def login_form():
    return f"""
        <h1>로그인폼</h1>
        <form action='/login_action' method='POST'>
            회원ID : <input name="mid"><br>
            회원비번 : <input type='passwprd' name='mpw'><br>
            <input type='submit' value='로그인'>
        </form>
    """
# 로그인 동작
count_dict = dict() 
@app.route("/login_action",methods=["POST"])
def login_action():
    mid = request.form.get("mid")
    mpw = request.form.get("mpw")
    #현재상태가 로그인이면 중지
    if session.get("mid") != None:
        return f"{mid}는 현재 로그인중입니다"
    if mpw == 'p1':
        cnt = count_dict.get(mid,0) #없으면 0
        cnt += 1
        count_dict[mid] = cnt # 저장
        session["mid"] = mid
        return f"""
            로그인 성공:cnt={cnt}<br>
            <a href='/my_info'>로그인정보 출력</a> <br>
            """
    return f"로그인 실패"

#로그아웃
@app.route("/logout")
def logout():
    session.clear()
    return f"""
        로그아웃완료<br> 
        <a href='/login_form'>로그인하기</a> <br>
        <a href='/my_info'>로그인정보 출력</a> <br>
        """

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
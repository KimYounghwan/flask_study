# app.py 파일 생성
from flask import Flask  # Flask 클래스를 flask 모듈에서 가져옴

# Flask 애플리케이션 객체 생성
# __name__은 현재 파일의 이름을 의미함. Flask가 템플릿과 정적 파일의 위치를 찾는 기준점
app = Flask(__name__)

# 데코레이터: URL 경로('/')에 대한 요청이 오면 아래 함수를 실행하라는 의미
@app.route('/')
def hello():
    # 브라우저에 보여줄 문자열 반환
    return '<h1>안녕하세요, Flask!</h1>'

@app.route("/about")
def about():
    return "<h2>김영환입니다</h2>"

#  /greet/홍길동  -> 안녕~ 홍길동님
@app.route("/greet/")
@app.route("/greet/<nm>")
def greet(nm="KIM"):
    return f"안녕~ {nm}님"

# @app.route("/greet/")
# def greet2():
#     return f"안녕~"


# 이 파일을 직접 실행했을 때만 서버가 시작되도록 함
# 다른 파일에서 import할 때는 서버가 실행되지 않음 (중요!)
if __name__ == '__main__':
    # debug=True: 코드 수정 시 자동으로 서버가 재시작됨 (개발할 때만 사용!)
    app.run(debug=True)
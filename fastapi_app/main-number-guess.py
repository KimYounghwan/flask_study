# 숫자맞추기 게임
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용 (개발용)
    allow_methods=["*"],  # 모든 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

import random
# 1~100사이 난수
com_num = random.randint(1,100)

@app.get("/")
def root():
    return {'message':'게임준비완료. 접근 url은 /guess/숫자 '}

@app.get("/guess/{num}")
def guess(num: int = 0):
    global com_num
    result = ""
    if com_num == num:
        result = "정답입니다.숫자변경했습니다."
        com_num = random.randint(1,100)
    elif com_num < num:
        result = "낮춰주세요"
    else:
        result = "높여주세요"
    return {'result':result}

# ..../guess2?num=50
@app.get("/guess2")
def guess2(num: int = 0):
    global com_num
    result = f"{num} "
    if com_num == num:
        result += "정답입니다.숫자변경했습니다."
        com_num = random.randint(1,100)
    elif com_num < num:
        result += "낮춰주세요"
    else:
        result += "높여주세요"
    return {'result':result}

count = 0
@app.get("/count_status")
def count_status():
    return {'count':count}

@app.get("/count_add/{num}")
def count_add(num:int):
    global count
    count += num
    return {'count':count}

@app.get("/count_minus/{num}")
def count_minus(num:int):
    global count
    count -= num
    return {'count':count}


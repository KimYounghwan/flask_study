"""
회원목록 - GET /members
회원등록 - POST /member
회원수정 - PUT /member/{mid}
회원삭제 - DELETE /member/{mid}
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import db_utils as stdentdb

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용 (개발용)
    allow_methods=["*"],  # 모든 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

@app.get("/members")
def members():
    mlist = stdentdb.get_all_students()
    return {"code":0,"data":mlist}

# ===== POST: 데이터 생성 =====
@app.post("/members")
def create_item(data:dict):
    res = stdentdb.create_student(data['name'],data['age'],data['gender'])
    if res :
        return {"code":0, "message":"등록 성공"}
    return {"code":1, "message":"등록 실패"}

# ===== POST: 데이터 수정 =====
@app.put("/members")
def update_item(data:dict):
    res = stdentdb.update_student(data['student_id'],data['name'],data['age'],data['gender'])
    if res :
        return {"code":0, "message":"수정 성공"}
    return {"code":1, "message":"수정 실패"}

# ===== GET: 데이터 조회 =====
@app.get("/members/{mid}")
def get_member(mid):
    res = stdentdb.get_student_by_id(mid)
    if res :
        return {"code":0, "data":res}
    return {"code":1, "message":"없거나 삭제된 id입니다"}    

# ===== DELETE: 데이터 삭제 =====
@app.delete("/members/{student_id}")
def delete_item(student_id: int):
    res = stdentdb.delete_student(student_id)
    if res :
        return {"code":0, "message":"삭제 성공"}
    return {"code":1, "message":"삭제 실패"}    

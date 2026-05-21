# main.py
from fastapi import FastAPI, Request,Body
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용 (개발용)
    allow_methods=["*"],  # 모든 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)
# ===== GET: 데이터 조회 =====
@app.get("/items")
def read_items():
    """
    GET /items
    모든 아이템 목록을 조회합니다
    """
    return {"items": ["사과", "바나나", "오렌지"]}

# ===== POST: 데이터 생성 =====
@app.post("/items")
def create_item():
    """
    POST /items
    새 아이템을 생성합니다
    (실습: 4회차에서 본문 데이터를 받는 방법 배움)
    """
    return {"message": "아이템이 생성되었습니다"}

# ===== PUT: 데이터 전체 수정 =====
@app.put("/items/{item_id}")
def update_item(item_id: int):
    """
    PUT /items/{item_id}
    특정 아이템을 전체 수정합니다
    """
    return {"item_id": item_id, "message": "아이템이 수정되었습니다"}

# ===== DELETE: 데이터 삭제 =====
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """
    DELETE /items/{item_id}
    특정 아이템을 삭제합니다
    """
    return {"item_id": item_id, "message": "아이템이 삭제되었습니다"}
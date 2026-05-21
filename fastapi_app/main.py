from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def hello():
    return {'message':'안녕~'}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    """
    아이템 ID를 받아서 해당 아이템 정보를 반환
    item_id: int → 타입 힌팅으로 자동 검증
    """
    return {"item_id": item_id, "name": f"아이템 {item_id}"}


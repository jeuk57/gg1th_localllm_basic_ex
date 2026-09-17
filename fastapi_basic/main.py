from fastapi import FastAPI

from pydantic import BaseModel, HttpUrl
from typing import Optional

# FastAPI 객체 생성
app = FastAPI()

# http://localhost:8000/
# http://127.0.0.1:8000/
@app.get("/")
async def read_root():
    # 비즈니스 로직 
    data = "db에서 데이터 읽어오기"
    return {"message": data}

# http://127.0.0.1:8000/items/
@app.get("/items")
def read_item():
    item_id = 1
    q = "사과"
    return {"item_id": item_id, "q": q}

# http://127.0.0.1:8000/items/300?q=아이스크림
# http://127.0.0.1:8000/items/100?q=사과
# http://127.0.0.1:8000/items/200?q=배
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
# def read_item(item_id, q):
    # 비즈니스 로직 처리
    print(f"item_id: {item_id}, q: {q}")

    return {"item_id": item_id, "q": q}

#http://localhost:8000/user_info/1234?q=je
# 위 url로 하면 안됨, 포스트는 아래처럼 url에 쿼리스트링을 붙이면 안됨
# q는 body에 담아서 보내야함
# http://localhost:8000/user_info/1234
@app.post("/user_info/{user_id}")
def create_user(user_id: int, q: str | None = None):
    # 비즈니스 로직 처리
    print(f"user_id: {user_id}, q: {q}")

    return {"user_id": user_id, "q": q}

# DTO : 데이터 전송 객체
class UserCreate(BaseModel):
    username: str
    password: str
    avatar_url: Optional[HttpUrl] = None
    user_fullname: Optional[str] = None

@app.post("/user_info/")
def create_user(user: UserCreate):
    # 비즈니스 로직
    print(f"username: {user.username}")
    print(f"avatar_url: {user.avatar_url}")
    print(f"user_fullname: {user.user_fullname}")

    return user
    # return {"user": user}
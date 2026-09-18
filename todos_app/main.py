from fastapi import FastAPI, Form, Depends, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session
import uvicorn
import os

from database import engine, SessionLocal, Base
import models

# models에 정의한 모든 클래스, 연결한 DB엔진에 테이블로 생성
Base.metadata.create_all(bind=engine)


# FastAPI() 객체 생성
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        # 마지막에 무조건 닫음
        db.close()


abs_path = os.path.dirname(os.path.realpath(__file__))

# template/ 폴더 식별 객체
templates = Jinja2Templates(directory=f"{abs_path}/template")

# static/ 폴더를 fastapi에서 인식할 수 있도록 마운트시킴
app.mount("/static", StaticFiles(directory=f"{abs_path}/static"), name="static")

# http://localhost:8000/
@app.get("/")
def home(request: Request,
         db_ss: Session = Depends(get_db)
         ):
    # 테이블 조회
    todos_list = db_ss.query(models.Todo).order_by(models.Todo.id.desc()).all()
    return templates.TemplateResponse(
        request = request,
        name = "index.html",
        context={ "todos": todos_list}
    )

# todo 데이터를 받아서 db 테이블에 저장하기
# http://localhost:8000/add
@app.post("/add")
def add(request: Request,
        task: str = Form(...),
        db_ss: Session = Depends(get_db)
        ):
    # task 데이터를 받고, Todo클래스를 통해서 테이블과 연결된 객체 생성
    todo = models.Todo(task=task)

    # todos 테이블에 task추가
    db_ss.add(todo)

    # 테이블에 반영
    db_ss.commit()

    # 엔드포인트 함수 home으로 redirect
    return RedirectResponse(url=app.url_path_for("home"),
                            status_code=status.HTTP_303_SEE_OTHER)


# todo 수정할 레코드 조회
@app.get("/edit/{todo_id}")
def edit(request: Request,
         todo_id: int,
         db_ss: Session = Depends(get_db)
         ):
    # todo_id 조회
    todo = db_ss.query(models.Todo).filter(models.Todo.id == todo_id).first()

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    # edit.html 하단의 전체 목록도 같이 보여주기 위해 조회
    todos_list = db_ss.query(models.Todo).order_by(models.Todo.id.desc()).all()

    # edit 폼에 렌더링 -> 리턴
    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={"todo": todo, "todos": todos_list}
    )


# todo 수정 내용 반영
@app.post("/edit/{todo_id}")
def update(todo_id: int,
           task: str = Form(...),
           completed: bool = Form(False),
           db_ss: Session = Depends(get_db)
           ):
    # 요청 수정 처리
    todo = db_ss.query(models.Todo).filter(models.Todo.id == todo_id).first()

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo.task = task
    todo.completed = completed
    db_ss.commit()

    return RedirectResponse(url=app.url_path_for("home"),
                            status_code=status.HTTP_303_SEE_OTHER)


# todo 삭제
@app.post("/delete/{todo_id}")
def delete(todo_id: int,
           db_ss: Session = Depends(get_db)
           ):
    todo = db_ss.query(models.Todo).filter(models.Todo.id == todo_id).first()

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db_ss.delete(todo)
    db_ss.commit()

    return RedirectResponse(url=app.url_path_for("home"),
                            status_code=status.HTTP_303_SEE_OTHER)



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

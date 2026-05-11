# FastAPI imports
from fastapi import Request, APIRouter, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from uuid import uuid4

router = APIRouter()

templates = Jinja2Templates("app/templates")

todos = []


# Routes
@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html.j2")


@router.post("/todos", response_class=HTMLResponse)
def add_todo(request: Request, title: Annotated[str, Form()]):

    todo = {"id": uuid4(), "title": title, "completed": False}
    todos.append(todo)

    return templates.TemplateResponse(
        request=request, name="/partials/todo_item.html.j2", context={"todo": todo}
    )

@router.delete('/todos/{todo_id}', response_class=HTMLResponse)
def delete_todo(todo_id: str):
    global todos

    todos = [todo for todo in todos if todo['id'] != todo_id]
    return HTMLResponse(content='')
# FastAPI imports
from fastapi import Request, APIRouter, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from sqlmodel import Session
from app.database import get_session
from app.models.todo import Todo

router = APIRouter()
templates = Jinja2Templates("app/templates")

todos = []

def get_stats_data():

    total = len(todos)

    completed = len([t for t in todos if t["completed"]])

    progress = int((completed / total) * 100) if total > 0 else 0

    return {
        "total": total,
        "completed": completed,
        "progress": progress,
    }


# Routes
@router.get("/", response_class=HTMLResponse)
def index(request: Request, filter: str = "all"):

    if filter == "completed":
        filtered_todos = [todo for todo in todos if todo["completed"]]

    elif filter == "active":
        filtered_todos = [todo for todo in todos if not todo["completed"]]

    else:
        filtered_todos = todos

    template = (
        "partials/todo_list.html.j2"
        if request.headers.get("hx-request")
        else "index.html.j2"
    )

    return templates.TemplateResponse(
        request=request,
        name=template,
        context={
            "todos": filtered_todos,
            **get_stats_data(),
        },
    )


@router.post("/todos", response_class=HTMLResponse)
def add_todo(request: Request, title: Annotated[str, Form()], session: Session = Depends(get_session)):

    todo = Todo(
        title= title,
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)
    
    # todo = {"id": str(uuid4()), "title": title, "completed": False}
    # todos.append(todo)

    response = templates.TemplateResponse(
        request=request, name="/partials/todo_item.html.j2", context={"todo": todo}
    )

    response.headers["HX-Trigger"] = "todosChanged"

    return response


@router.delete("/todos/{todo_id}", response_class=HTMLResponse)
def delete_todo(todo_id: str):
    global todos

    todos = [todo for todo in todos if todo["id"] != todo_id]
    response = HTMLResponse(content="")

    response.headers["HX-Trigger"] = "todosChanged"

    return response


@router.post("/todos/{todo_id}/toggle", response_class=HTMLResponse)
def toggle_todo(request: Request, todo_id: str):

    todo = next(todo for todo in todos if todo["id"] == todo_id)

    todo["completed"] = not todo["completed"]

    response = templates.TemplateResponse(
        request=request, name="/partials/todo_item.html.j2", context={"todo": todo}
    )

    response.headers["HX-Trigger"] = "todosChanged"

    return response


@router.get("/stats", response_class=HTMLResponse)
def get_stats(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="partials/stats.html.j2",
        context={
            **get_stats_data(),
        },
    )

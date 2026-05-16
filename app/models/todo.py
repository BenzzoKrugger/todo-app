from sqlmodel import Field, SQLModel


class Todo(SQLModel, table=True):
    id: str | None = Field(default=None, primary_key=True)
    title: str
    completed: bool = False
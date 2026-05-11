# FastAPI imports
from fastapi import FastAPI
from app.routes.todo import router


# Initialize app
app = FastAPI()
app.include_router(router=router)


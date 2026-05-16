# FastAPI imports
from fastapi import FastAPI
from app.routes.todo import router
from app.database import create_db_and_tables 


# Initialize app
app = FastAPI()
app.include_router(router=router)

# Create DB
create_db_and_tables()


from fastapi import FastAPI
from pydantic import BaseModel
from routes import auth, health

class User(BaseModel):
    name: str
    age: int
    email : str


app = FastAPI()

app.include_router(auth.router)
app.include_router(health.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_idddddd": item_id}

@app.post("/users/")
async def create_user(user: User):
    return {"message": f"User {user.name} created successfully!"}
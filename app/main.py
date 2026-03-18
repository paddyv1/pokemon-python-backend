from fastapi import FastAPI
from app.routes import auth, health
##todo implement middleware
##todo implement logging
##todo implement rate limiting


app = FastAPI()

app.include_router(auth.router, prefix="/api")
app.include_router(health.router, prefix="/api")

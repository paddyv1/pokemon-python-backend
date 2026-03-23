from fastapi import FastAPI
from app.routes import auth, health, team
##todo implement middleware
##todo implement logging
##todo implement rate limiting


app = FastAPI(
    docs_url="/api/docs",            # Swagger UI location
    openapi_url="/api/openapi.json"  # OpenAPI schema location
)

app.include_router(auth.router, prefix="/api")
app.include_router(health.router, prefix="/api")
app.include_router(team.router, prefix="/api")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints import books, users, borrowing, fines, sections
from app.core.database import engine, Base
from app.core.exceptions import http_error_handler, validation_exception_handler
from fastapi.exceptions import RequestValidationError, HTTPException

# Create tables if not exist (simplest for dev without running manual migrations command first)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception Handlers
app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Routers
app.include_router(books.router, prefix=f"{settings.API_V1_STR}/books", tags=["books"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(borrowing.router, prefix=f"{settings.API_V1_STR}/borrowing", tags=["borrowing"])
app.include_router(fines.router, prefix=f"{settings.API_V1_STR}/fines", tags=["fines"])
app.include_router(sections.router, prefix=f"{settings.API_V1_STR}/sections", tags=["sections"])

@app.get("/")
def root():
    return {"message": "Welcome to Library API"}

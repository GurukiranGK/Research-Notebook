from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.routes import auth, chat, documents, notebooks, protected, search


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def internal_error_handler(_request, exc):
    print(exc)
    return JSONResponse(status_code=500, content={"error": "Internal Server Error"})


@app.exception_handler(HTTPException)
async def http_error_handler(_request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


app.include_router(protected.router)
app.include_router(auth.router)
app.include_router(notebooks.router)
app.include_router(documents.router)
app.include_router(search.router)
app.include_router(chat.router)

from fastapi import FastAPI
from dotenv import load_dotenv
import os
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware

load_dotenv(dotenv_path=".env")

print("OPENAI_API_KEY in main:", bool(os.getenv("OPENAI_API_KEY")))

app = FastAPI(
    title="Multi-Agent Chat System",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

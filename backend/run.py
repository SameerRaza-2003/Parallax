import os
from dotenv import load_dotenv
import uvicorn

# FORCE load .env before anything else
load_dotenv(dotenv_path=".env")

print("OPENAI_API_KEY loaded:", bool(os.getenv("OPENAI_API_KEY")))

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

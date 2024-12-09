import sys
from pathlib import Path

from fastapi import FastAPI
import uvicorn

sys.path.append(str(Path(__file__).parent.parent))

from src.api.author import router as router_author

app = FastAPI()

app.include_router(router_author)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)


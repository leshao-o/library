import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import uvicorn

sys.path.append(str(Path(__file__).parent.parent))

from src.api.author import router as router_author
from src.api.book import router as router_book
from src.api.borrow import router as router_borrow
from src.init_cache import redis_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    print("Initialized FastAPI cache")
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    yield
    await redis_manager.close()


app = FastAPI(lifespan=lifespan)

app.include_router(router_author)
app.include_router(router_book)
app.include_router(router_borrow)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)

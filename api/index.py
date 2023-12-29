from fastapi import Depends, FastAPI, Request
from fastapi.responses import RedirectResponse
from redis.asyncio import Redis

from api.deps import get_redis
from api.helper import gen_note_id, render_note

app = FastAPI()


@app.get("/")
async def root():
    return RedirectResponse(f"/{gen_note_id()}")


@app.get("/{id}")
async def note(id: str, redis: Redis = Depends(get_redis, use_cache=True)):
    content = (raw := await redis.get(f"note:{id}")) and raw.decode()
    return render_note(content)


@app.post("/{id}")
async def note_post(
    id: str, request: Request, redis: Redis = Depends(get_redis, use_cache=True)
):
    content = (await request.body()).decode()
    await redis.set(f"note:{id}", content)
    return ""

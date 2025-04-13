import redis.asyncio as redis
from math import ceil
from contextlib import asynccontextmanager
from decouple import config
from fastapi import (
    FastAPI,
    HTTPException,
    Request,
    Response
)
from fastapi_limiter import FastAPILimiter

REDIS_URL = config('REDIS_URL')

async def rate_limit_exceeded_handler(
        request: Request,
        response: Response,
        pexpire: int
):
    expires_in = ceil(pexpire / 1000)
    raise HTTPException(status_code=429, detail="Too many requests, try again soon. ", headers={"Retry-After": str(expires_in)})


async def rate_limit_identifier(request: Request):
    # ToDo: This we might need to change as per the API or API user
    # return f"user:1:{request.scope['path']}". # This is to edit the endpoint: this includes user and path
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0]
    return request.client.host + ":" + request.scope["path"]


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis_connection = redis.from_url(REDIS_URL,
                                      # encoding="utf-8"
                                      )
    await FastAPILimiter.init(
        redis_connection,
        identifier=rate_limit_identifier,
        http_callback=rate_limit_exceeded_handler
    )
    yield
    await FastAPILimiter.close()
import logging
import os
from functools import cache

from fastapi import FastAPI, Response, status
from redis import Redis, RedisError

app = FastAPI()

logging.basicConfig()


@app.get("/")
def index(response: Response):
    try:
        page_views = redis().incr("page_views")
    except RedisError:
        logging.exception("Redis error")

        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return "Sorry, something went wrong \N{thinking face}"
    else:
        return f"This page has been seen {page_views} times."


@cache
def redis():
    return Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379)

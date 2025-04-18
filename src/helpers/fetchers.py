import httpx
from fastapi import HTTPException


async def fetch_file_async(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != httpx.codes.OK:
            raise HTTPException(status_code=response.status_code)
        return response.content
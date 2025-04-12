from typing import Union

from fastapi import FastAPI
import helpers
app = FastAPI()


@app.get("/")
def read_root():
    # helpers.generate_image
    return {"Hello": "World"}


@app.post("/generate")
def generate_image(item_id: Union[int, str]):
    return {"item_id": item_id}
from functools import lru_cache
import replicate
from replicate.client import Client
from decouple import config

REPLICATE_API_TOKEN = config('REPLICATE_API_TOKEN')
REPLICATE_MODEL = config('REPLICATE_MODEL')
REPLICATE_MODEL_VERSION = config('REPLICATE_MODEL_VERSION')


@lru_cache
def get_replicate_client() -> replicate.Client:
    return Client(api_token=REPLICATE_API_TOKEN)

@lru_cache
def get_replicate_model_version() -> str:
    replicate_client = get_replicate_client()
    replicate_model = replicate_client.models.get(REPLICATE_MODEL)
    replicate_version = replicate_model.versions.get(REPLICATE_MODEL_VERSION)
    return replicate_version

def generate_image(prompt: str):
    input_args = {
        "prompt": prompt,
        "num_outputs": 2,
        "output_format": "jpg",
    }
    replicate_client = get_replicate_client()
    replicate_version = get_replicate_model_version()
    pred = replicate_client.predictions.create(
        version=replicate_version,
        input=input_args,
    )

    return {
        "id": pred.id,
        "status": pred.status
    }

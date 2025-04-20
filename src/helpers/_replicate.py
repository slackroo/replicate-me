from functools import lru_cache
import replicate
from replicate.client import Client
from decouple import config
from replicate.exceptions import ReplicateError

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


def generate_image(prompt: str,
                   require_trigger_word: bool = True,
                   trigger_word: str = "TOK",
                   ):
    if require_trigger_word:
        if trigger_word not in prompt:
            raise Exception(f"Trigger word: {trigger_word} not found in prompt")

    input_args = {
        "prompt": prompt,
        "num_outputs": 2,
        "output_format": "jpg",
    }
    replicate_client = get_replicate_client()
    replicate_version = get_replicate_model_version()
    return replicate_client.predictions.create(
        version=replicate_version,
        input=input_args,
    )


# def list_prediction_results(model=REPLICATE_MODEL,
#                             version=REPLICATE_MODEL_VERSION,
#                             status=None,
#                             max_size=500
#                             ) -> list:
#     replicate_client = get_replicate_client()
#     preds = replicate_client.predictions.list()
#     results = list(preds.results)
#     while preds.next:
#         _preds = replicate_client.predictions.list(preds.next)
#         results += list(_preds.results)
#         if len(results) > max_size:
#             break
#     results = [
#         {
#             "url": f"/predictions/{x.id}",
#             "status": x.status,
#             "created_at": x.created_at,
#             "completed_at": x.completed_at,
#         }
#         for x in results if x.model == model and x.version == version
#     ]  # Todo: we can improve this via pydantic
#
#     if status is not None:
#
#         results = [
#             x
#             for x in results if x['status'] == status
#         ]
#
#     return results


def list_prediction_results(model=REPLICATE_MODEL,
                            version=REPLICATE_MODEL_VERSION,
                            status=None,
                            max_size=500
                            ):
    replicate_client = get_replicate_client()
    preds = replicate_client.predictions.list()
    results = list(preds.results)
    while preds.next:
        _preds = replicate_client.predictions.list(preds.next)
        results += list(_preds.results)
        if len(results) > max_size:
            break
    results = [x for x in results if x.model == model and x.version == version]

    if status is not None:
        results = [x for x in results if x.status == status]

    return results


def get_prediction_details(
        prediction_id=None,
):
    replicate_client = get_replicate_client()
    try:
        pred = replicate_client.predictions.get(prediction_id)
    except ReplicateError:
        return None, 404
    except:
        return None, 500

    return pred, 200

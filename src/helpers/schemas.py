from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel

class PredictionCreateModel(BaseModel):
    id:str
    url:str
    status:str

    @classmethod
    def from_replicate(cls, data: Dict[str, Any]) -> "PredictionCreateModel":
        # print(data)

        _id = data.get('id')
        url = f'/predictions/{_id}'
        return cls(
            id=_id,
            url=url,
            status=data.get('status'),
        )


# {
# #             "url": f"/predictions/{x.id}",
# #             "status": x.status,
# #             "created_at": x.created_at,
# #             "completed_at": x.completed_at,
# #         }

class PredictionListModel(BaseModel):
    id:str
    url:str
    status:str
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    @classmethod
    def from_replicate(cls, data: Dict[str, Any]) -> "PredictionListModel":
        # print(data)

        _id = data.get('id')
        url = f'/predictions/{_id}'
        return cls(
            id=_id,
            url=url,
            status=data.get('status'),
            created_at=data.get('created_at'),
            started_at=data.get('started_at') or None,
            completed_at=data.get('completed_at') or None,
        )


class PredictionDetailModel(BaseModel):
    id: str
    url: str
    model: str
    version: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    files: Optional[List[str]] = []
    num_outputs: Optional[int] = 0

    @classmethod
    def from_replicate(cls, data: Dict[str, Any]) -> "PredictionDetailModel":
        # print(data)

        _id = data.get('id')
        url = f'/predictions/{_id}'
        _input = data.get('input') or {}
        num_outputs = _input.get('num_outputs') or 0
        _output = data.get('output') or []
        output_names = [Path(x) for x in _output]
        files = []
        for idx, output_path in enumerate(output_names):
            suffix = output_path.suffix
            files.append(
                f"{url}/files/{idx}{suffix}"
            )
        return cls(
            id=_id,
            url=url,
            model=data.get('model'),
            version=data.get('version'),
            created_at=data.get('created_at'),
            completed_at=data.get('completed_at') or None,
            files=files,
            status=data.get('status'),
            num_outputs=num_outputs
        )

from pydantic import BaseModel, Field


PayloadRequest = dict[str, list[str]]


class PayloadCreateResponse(BaseModel):
    id: int
    message: str = "payload created"


class TransformsResponse(BaseModel):
    output: str
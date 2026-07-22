from pydantic import BaseModel

class DrugInteractionRequest(BaseModel):
    drugs: list[str]
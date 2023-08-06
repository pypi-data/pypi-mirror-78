from typing import List

from pydantic.main import BaseModel


class NivaUser(BaseModel):
    id: int
    email: str
    displayName: str
    provider: str
    roles: List[str]

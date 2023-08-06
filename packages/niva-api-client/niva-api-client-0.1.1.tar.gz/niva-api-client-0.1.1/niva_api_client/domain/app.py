from datetime import datetime
from typing import List

from pydantic.main import BaseModel


class NivaApp(BaseModel):
    id: str
    title: str
    description: str
    createTime: datetime
    updateTime: datetime
    creator: str
    public: bool
    subdomain: str
    # heroImage: str
    # logo: str
    subheader: str
    gitRepo: str
    roles: List[str]

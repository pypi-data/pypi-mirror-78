from datetime import datetime

from pydantic import BaseModel

from niva_api_client.domain.niva_user import NivaUser


class TokenRefreshPayload(BaseModel):
    tokenId: int
    refreshedTime: datetime
    user: NivaUser


class AccessToken(BaseModel):
    tokenString: str
    payload: TokenRefreshPayload

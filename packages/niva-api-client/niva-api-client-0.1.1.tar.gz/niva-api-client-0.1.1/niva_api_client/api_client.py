import logging
import os
from typing import Dict
from uuid import uuid4
import poetry_version

import requests

from niva_api_client.environments import PORT_URL_PRODUCTION
from niva_api_client.domain.access_token import AccessToken


def access_token(token: str) -> AccessToken:
    response = requests.get(
        f"{PORT_URL_PRODUCTION}/api/token/refresh",
        headers={"Authorization": f"Bearer {token}"},
    )
    response.raise_for_status()
    print(response.json())

    return AccessToken(**response.json())


def api_headers(token: AccessToken) -> Dict:
    """
    Generates API headers to be used when interacting with NIVA API's:

    - Authorization header
    - Trace-Id to be used for logging and debugging purposes
    - User-Agent identifying the version of this library (niva-api-client-python/X.Y.Z
    """
    api_client_version = poetry_version.extract(source_file=__file__)
    trace_id = str(uuid4())
    return {
        "Authorization": f"Bearer {token.tokenString}",
        "Trace-Id": trace_id,
        "User-Agent": f"niva-api-client-python/{api_client_version}",
    }


if __name__ == "__main__":
    token = os.environ["NIVA_REFRESH_TOKEN"]
    access_token(token)

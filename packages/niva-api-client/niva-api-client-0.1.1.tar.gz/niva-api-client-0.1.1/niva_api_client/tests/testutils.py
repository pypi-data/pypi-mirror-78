from datetime import datetime
from uuid import uuid4

from niva_api_client.domain.app import NivaApp


def create_niva_app(
    title="someapp",
    description="Dummy app description",
    subheader="Some header",
    public=False,
    roles=["niva"],
) -> NivaApp:
    return NivaApp(
        id=str(uuid4()),
        title=title,
        description=description,
        creator=str(uuid4()),
        createTime=datetime.now(),
        updateTime=datetime.now(),
        subdomain=title,
        public=public,
        subheader=subheader,
        gitRepo="https://github.com/NIVANorge/niva-api-client-python",
        roles=roles,
    )

from urllib.parse import urlparse, urlsplit, urlunparse

from niva_api_client.domain.app import NivaApp
from niva_api_client.environments import PORT_URL_PRODUCTION


def app_url(app: NivaApp, port_url=PORT_URL_PRODUCTION) -> str:
    return subdomain_for(app.subdomain, port_url)


def subdomain_for(subdomain: str, url: str) -> str:
    url_list = list(urlparse(url))
    url_list[1] = f"{subdomain}.{url_list[1]}"

    return urlunparse(url_list)

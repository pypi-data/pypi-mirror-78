from niva_api_client.tests.testutils import create_niva_app
from niva_api_client.url_utils import app_url, subdomain_for


def test_app_subdomain():
    app = create_niva_app(title="awesomeapp")
    url = app_url(app)
    assert url == "https://awesomeapp.data.niva.no"


def test_subdomain_for():
    subdomain_nrk = subdomain_for("tv", "https://nrk.no")
    assert subdomain_nrk == "https://tv.nrk.no"

    many_levels = subdomain_for("many.levels.with-dashes", "http://niva.no")
    assert many_levels == "http://many.levels.with-dashes.niva.no"

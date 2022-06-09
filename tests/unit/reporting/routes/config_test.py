from reporting.app import create_app


def test_config(mocker):
    mocker.patch(
        "reporting.settings.REPORTING_CONFIG_FILE",
        "tests/data/reporting-dashboard.conf",
    )
    settings = {
        "PREFERRED_URL_SCHEME": "https",
        "SECRET_KEY": "fake",
    }
    app = create_app(settings)
    client = app.test_client()
    ret = client.get("/api/v1/config", follow_redirects=False)
    assert ret.status_code == 200
    ret_json = ret.json
    assert ret_json["console_url"] == "https://localhost:7473"
    for key in ["queries", "dashboard", "reports"]:
        assert key in ret_json["config"].keys()
    assert ret_json["config"]["version"] == 1
    assert "$schema" in ret_json["schema"].keys()

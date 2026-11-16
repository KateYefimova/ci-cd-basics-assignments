import app as app_module


def test_health_answers_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_data(as_text=True) == "ok\n"


def test_ready_reports_file_store(client):
    r = client.get("/ready")
    assert r.status_code == 200
    body = r.get_json()
    assert body["ready"] is True
    assert body["store"].startswith("file:")


def test_ready_is_503_when_store_unusable(client, tmp_path, monkeypatch):
    blocker = tmp_path / "blocker"
    blocker.write_text("i am a file, not a directory")
    monkeypatch.setattr(app_module, "COUNTER_FILE", blocker / "visits.txt")
    r = client.get("/ready")
    assert r.status_code == 503
    assert r.get_json()["ready"] is False


def test_visits_starts_at_one_and_counts_up(client):
    assert client.get("/visits").get_json() == {"visits": 1, "store": "file"}
    assert client.get("/visits").get_json()["visits"] == 2
    assert client.get("/visits").get_json()["visits"] == 3


def test_visits_persists_to_the_counter_file(client):
    client.get("/visits")
    client.get("/visits")
    assert app_module.COUNTER_FILE.read_text().strip() == "2"


def test_visits_continues_from_existing_file(client):
    app_module.COUNTER_FILE.parent.mkdir(parents=True, exist_ok=True)
    app_module.COUNTER_FILE.write_text("41")
    assert client.get("/visits").get_json()["visits"] == 42


def test_visits_is_503_when_store_unusable(client, tmp_path, monkeypatch):
    blocker = tmp_path / "blocker"
    blocker.write_text("not a directory")
    monkeypatch.setattr(app_module, "COUNTER_FILE", blocker / "visits.txt")
    r = client.get("/visits")
    assert r.status_code == 503
    assert "error" in r.get_json()


class _FakeResponse:
    def raise_for_status(self):
        pass

    def json(self):
        return {"price": 1999, "currency": "EUR"}


def test_price_returns_partner_data(client, monkeypatch):
    seen = {}

    def fake_get(url, timeout):
        seen["url"] = url
        return _FakeResponse()

    monkeypatch.setattr(app_module.requests, "get", fake_get)
    r = client.get("/price/MK-II")
    assert r.status_code == 200
    assert r.get_json()["price"] == 1999
    assert seen["url"].endswith("/v1/catalog/MK-II")


def test_price_is_502_when_partner_is_down(client, monkeypatch):
    def boom(url, timeout):
        raise app_module.requests.ConnectionError("partner is down")

    monkeypatch.setattr(app_module.requests, "get", boom)
    r = client.get("/price/MK-II")
    assert r.status_code == 502
    assert r.get_json()["error"] == "ConnectionError"



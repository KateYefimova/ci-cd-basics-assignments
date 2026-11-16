import os
import sys
from pathlib import Path

os.environ.pop("DATABASE_URL", None)
os.environ.setdefault("COUNTER_FILE", "/tmp/catshop-test-visits.txt")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest 

import app as app_module  


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "COUNTER_FILE", tmp_path / "data" / "visits.txt")
    monkeypatch.setattr(app_module, "DATABASE_URL", None)
    app_module.app.config["TESTING"] = True
    return app_module.app.test_client()
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_ok():
    r = client.get("/")
    assert r.status_code == 200

def test_invalid_input_returns_422():
    r = client.get("/predict/flood-risk", params={"slope": 999})
    assert r.status_code == 422      # slope must be 0..90

# run the whole file with:  pytest -v

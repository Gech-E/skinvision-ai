def test_root_healthy(client):
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("message") == "SkinVision AI API is running"



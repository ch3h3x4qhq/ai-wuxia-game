from fastapi.testclient import TestClient

from app.main import app


def test_run_seed_reproducible() -> None:
    client = TestClient(app)
    payload = {"seed": 123456, "name": "测试侠"}
    first = client.post("/api/runs/new", json=payload)
    assert first.status_code == 200
    run_a = first.json()

    second = client.post("/api/runs/new", json=payload)
    assert second.status_code == 200
    run_b = second.json()

    assert run_a["seed"] == run_b["seed"] == 123456
    assert run_a["node_map"] == run_b["node_map"]

    save_resp = client.post(f"/api/runs/{run_a['run_id']}/save")
    assert save_resp.status_code == 200
    assert save_resp.json()["ok"] is True

    loaded = client.post(f"/api/runs/{run_a['run_id']}/load")
    assert loaded.status_code == 200
    loaded_json = loaded.json()
    assert loaded_json["run_id"] == run_a["run_id"]
    assert loaded_json["player"]["name"] == "测试侠"

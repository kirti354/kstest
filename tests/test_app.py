from fastapi.testclient import TestClient

from src import app as app_module


client = TestClient(app_module.app)


def test_get_activities_returns_activity_data():
    response = client.get("/activities")

    assert response.status_code == 200
    body = response.json()
    assert "Chess Club" in body
    assert "participants" in body["Chess Club"]


def test_signup_accepts_valid_activity():
    original_participants = app_module.activities["Chess Club"]["participants"].copy()

    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "verification@example.com"},
    )

    assert response.status_code == 200
    assert "verification@example.com" in app_module.activities["Chess Club"]["participants"]

    app_module.activities["Chess Club"]["participants"] = original_participants


def test_signup_returns_not_found_for_unknown_activity():
    response = client.post(
        "/activities/Unknown/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}

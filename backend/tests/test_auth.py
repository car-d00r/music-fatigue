import pytest
from requests import Session
import subprocess
import time
from app import store

BASE_URL = "http://localhost:8000"

@pytest.fixture(scope="module")
def req_session():
    return Session()

@pytest.fixture(scope="module")
def server():
    process = subprocess.Popen(["uvicorn", "app:app", "--port", "8000"])
    time.sleep(2)  # Give the server time to start
    yield
    process.terminate()
    process.wait()

def test_hello_world(server, req_session):
    response = req_session.get(BASE_URL + "/")
    assert response.status_code == 200
    response = req_session.get("/".join([BASE_URL, "login"]))
    assert response.status_code == 200
    mock_code = "test_auth_code"
    callback_url = f"{BASE_URL}/callback?code={mock_code}"
    response = req_session.get(callback_url)
    assert response.status_code == 200

    # Step 4: Manually set the session ata
    session_id = req_session.cookies.get('session')  # Get the session ID from cookies
    if session_id:
        store.set(session_id, {
            "spotify_token": {
                "access_token": "mock_access_token",
                "refresh_token": "mock_refresh_token",
                "expires_at": int(time.time()) + 3600  # Set expiry to 1 hour from now
            }
        })

    response = req_session.get(f"{BASE_URL}/spotify/user")
    assert response.status_code == 200

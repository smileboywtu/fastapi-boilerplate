from fastapi.testclient import TestClient

from handlers.application import app_instance

client = TestClient(app_instance)

from app import app
import pytest

@pytest.fixture(scope="class")
def app_fix():
    app.config['TESTING'] = True
    return app.test_client()
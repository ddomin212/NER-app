"""
This module contains fixtures for the pytest testing framework.
"""
import pytest
from app import app


@pytest.fixture(scope="class")
def app_fix():
    """
    Set the app to test mode and return the client. This is useful for unit tests that
    don't need a client but need to test the client in order to make sure it's working correctly.

    @return The client to test with after running the tests in this case the app is
            running and ready to use
    """
    app.config["TESTING"] = True
    return app.test_client()

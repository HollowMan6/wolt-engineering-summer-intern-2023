"""Module defining fixtures that will be shared among all tests."""
import pytest
from src.app import create_app


@pytest.fixture()
def app():
  application = create_app()
  yield application


@pytest.fixture()
def client(app):  # pylint: disable=redefined-outer-name
  return app.test_client()


@pytest.fixture()
def runner(app):  # pylint: disable=redefined-outer-name
  return app.test_cli_runner()

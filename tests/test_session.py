"""Test Skaha Session API."""

from uuid import uuid4

import pytest

from skaha.session import Session


@pytest.fixture(scope="module")
def name():
    """Return a random name."""
    yield str(uuid4())


@pytest.fixture(scope="session")
def session():
    """Test images."""
    session = Session()
    yield session
    del session


def test_session_with_kind(session):
    """Test fetching images with kind."""
    assert session.fetch(kind="headless") == []

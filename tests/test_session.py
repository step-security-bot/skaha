"""Test Skaha Session API."""

from time import sleep
from typing import Any, Dict, List
from uuid import uuid4

import pytest
from pydantic import ValidationError

from skaha.session import Session

pytest.IDENTITY: List[str] = []  # type: ignore


@pytest.fixture(scope="module")
def name():
    """Return a random name."""
    yield str(uuid4().hex[:7])


@pytest.fixture(scope="session")
def session():
    """Test images."""
    session = Session()
    yield session
    del session


def test_fetch_with_kind(session: Session):
    """Test fetching images with kind."""
    session.fetch(kind="headless")


def test_fetch_malformed_kind(session: Session):
    """Test fetching images with malformed kind."""
    with pytest.raises(ValidationError):
        session.fetch(kind="invalid")


def test_fetch_with_malformed_view(session: Session):
    """Test fetching images with malformed view."""
    with pytest.raises(ValidationError):
        session.fetch(view="invalid")


def test_fetch_with_malformed_status(session: Session):
    """Test fetching images with malformed status."""
    with pytest.raises(ValidationError):
        session.fetch(status="invalid")


def test_session_stats(session: Session):
    """Test fetching images with kind."""
    assert "instances" in session.stats().keys()


def test_create_session_with_malformed_kind(session: Session, name: str):
    """Test creating a session with malformed kind."""
    with pytest.raises(ValidationError):
        session.create(
            name=name,
            kind="invalid",
            image="ubuntu:latest",
            cmd="bash",
            replicas=1,
        )


def test_create_session_cmd_without_headless(session: Session, name: str):
    """Test creating a session without headless."""
    with pytest.raises(ValidationError):
        session.create(
            name=name,
            kind="notebook",
            image="ubuntu:latest",
            cmd="bash",
            replicas=1,
        )


def test_create_session(session: Session, name: str):
    """Test creating a session."""
    identity: List[str] = session.create(
        name=name,
        kind="headless",
        cores=1,
        ram=1,
        image="images.canfar.net/skaha/terminal:1.1.2",
        cmd="env",
        replicas=1,
        env={"TEST": "test"},
    )
    assert len(identity) == 1
    assert identity[0] != ""
    pytest.IDENTITY = identity  # type: ignore


def test_get_session_info(session: Session, name: str):
    """Test getting session info."""
    info: List[Dict[str, Any]] = [{}]
    attempt: int = 0
    while attempt < 10:
        sleep(6)
        info = session.info(pytest.IDENTITY)  # type: ignore
        if len(info) == 1:
            break
        attempt += 1
    assert info[pytest.IDENTITY[0]]["name"] == name  # type: ignore


def test_session_logs(session: Session, name: str):
    """Test getting session logs."""
    attempt: int = 0
    logs: Dict[str, str] = {}
    while attempt < 10:
        sleep(6)
        info = session.info(pytest.IDENTITY)  # type: ignore
        if info[0]["status"] == "Succeeded":
            break
    logs = session.logs(pytest.IDENTITY)  # type: ignore
    success = False
    for line in logs[pytest.IDENTITY[0]].split("\n"):  # type: ignore
        if "TEST=test" in line:
            success = True
            break
    assert success


def test_delete_session(session: Session, name: str):
    """Test deleting a session."""
    # Delete the session
    deletion = session.destroy(pytest.IDENTITY[0])  # type: ignore
    assert deletion == {pytest.IDENTITY[0]: True}  # type: ignore

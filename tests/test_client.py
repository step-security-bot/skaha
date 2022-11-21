"""Test Skaha Client API."""

import pytest
import requests

from pydantic import BaseModel
from skaha.client import SkahaClient
from skaha.exceptions import InvalidCertificateError, InvalidServerURL


def test_client_has_session_attribute():
    """Test if it SkahaClient object contains requests.Session attribute"""
    client = SkahaClient()
    assert hasattr(client, "session")
    assert isinstance(client.session, requests.Session)


def test_client_session():
    """Test SkahaClient object's session attribute contains ther right headers"""
    headers = [
        "X-Skaha-Server",
        "Content-Type",
        "Accept",
        "User-Agent",
        "Date",
        "X-Skaha-Version",
        "X-Skaha-Client-Python-Version",
        "X-Skaha-Client-Arch",
        "X-Skaha-Client-OS",
        "X-Skaha-Client-OS-Version",
        "X-Skaha-Client-Platform",
    ]
    client = SkahaClient()
    assert any(list(map(lambda h: h in client.session.headers.keys(), headers)))


def test_bad_server():
    """Test bad server."""
    with pytest.raises(InvalidServerURL):
        SkahaClient(server="abcdefd")


def test_bad_certificate():
    """Test bad certificate."""
    with pytest.raises(InvalidCertificateError):
        SkahaClient(certificate="abcdefd")


def test_bad_certificate_path():
    """Test bad certificate."""
    with pytest.raises(InvalidCertificateError):
        SkahaClient(certificate="/tmp/abcdefd")

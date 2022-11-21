"""Skaha Client."""
from os import environ
from pathlib import Path
from platform import machine, platform, python_version, release, system
from time import asctime, gmtime

from requests import Session
from validators import url
from typing import Optional, Type
from pydantic import BaseModel, Field, validator, root_validator

from skaha import __version__
from skaha.exceptions import InvalidCertificateError, InvalidServerURL


# @attrs
class SkahaClient(BaseModel):
    """SkahaClient is the base class for all other API clients.

    Args:
        BaseModel (pydantic.BaseModel): Pydantic BaseModel.

    Raises:
        InvalidServerURL: If the server URL is invalid.
        InvalidCertificateError: If the client is given an invalid certificate.

    Examples:
        >>> from skaha.client import SkahaClient
            class MyClient(SkahaClient):
                pass

    """

    server: str = Field(default="https://ws-uv.canfar.net/skaha", title="Server URL")
    certificate: str = Field(
        default="{HOME}/.ssl/cadcproxy.pem".format(HOME=environ["HOME"]), type=str,
        title="Certificate File"
    )
    timeout: int = Field(default=15, title="Timeout")
    session: Type[Session] = Field(default=Session())
    cert: Optional[str] = Field(default="")
    verify: Optional[bool] = Field(default=False)

    @root_validator
    def session_set_headers(cls, values):
        """Set headers to session object after all values has been obtained."""
        values["session"].headers.update({"X-Skaha-Server": values["server"]})
        values["session"].headers.update({"Content-Type": "application/json"})
        values["session"].headers.update({"Accept": "*/*"})
        values["session"].headers.update({"User-Agent": "skaha-client"})
        values["session"].headers.update({"Date": asctime(gmtime())})
        values["session"].headers.update({"X-Skaha-Version": __version__})
        values["session"].headers.update(
            {"X-Skaha-Client-Python-Version": python_version()}
        )
        values["session"].headers.update({"X-Skaha-Client-Arch": machine()})
        values["session"].headers.update({"X-Skaha-Client-OS": system()})
        values["session"].headers.update({"X-Skaha-Client-OS-Version": release()})
        values["session"].headers.update({"X-Skaha-Client-Platform": platform()})
        return values

    @root_validator
    def certificate_is_valid(cls, values):
        """Check the certificate."""
        if not Path(values["certificate"]).is_absolute():
            raise InvalidCertificateError("certificate must be an absolute path.")
        if not Path(values["certificate"]).is_file():
            raise InvalidCertificateError(f"{values['certificate']} does not exist.")
        values["session"].headers.update({"X-Skaha-Authentication-Type": "certificate"})
        values["cert"] = values["certificate"]
        values["verify"] = True
        return values

    @validator("server")
    def server_has_valid_url(cls, value, values):
        """Check if server is a valid url."""
        if not url(value):
            raise InvalidServerURL("Server must be a valid URL.")
        return value

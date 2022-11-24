"""Skaha Client."""
from os import environ, access, R_OK
from pathlib import Path
from platform import machine, platform, python_version, release, system
from time import asctime, gmtime

from requests import Session
from validators import url
from typing import Optional, Type
from pydantic import (
    BaseModel,
    Field,
    validator,
    root_validator,
    AnyHttpUrl,
    FilePath,
    ValidationError,
)
from pydantic.tools import parse_obj_as

from skaha import __version__
from skaha.exceptions import InvalidCertificateError, InvalidServerURL


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

    server: AnyHttpUrl = Field(
        default="https://ws-uv.canfar.net/skaha", title="Server URL", type=AnyHttpUrl
    )
    certificate: FilePath = Field(
        default="{HOME}/.ssl/cadcproxy.pem".format(HOME=environ["HOME"]),
        type=str,
        title="Certificate File",
    )
    timeout: int = Field(default=15, title="Timeout")
    session: Type[Session] = Field(default=Session())
    cert: Optional[str] = Field(default="")
    verify: Optional[bool] = Field(default=False)

    @validator("server", pre=True, always=True)
    def server_has_valid_url(cls, value):
        """Check if server is a valid url."""
        error = None
        try:
            value = parse_obj_as(AnyHttpUrl, value)
        except ValidationError as e:
            error = e
        if error:
            raise InvalidServerURL(f"Server must be a valid URL.")
        return value

    @validator("certificate", pre=True, always=True)
    def certificate_exists_and_is_readable(cls, value):
        """Check the certificate."""
        error = None
        try:
            value = parse_obj_as(FilePath, value)
        except ValidationError as e:
            error = e
        if error:
            raise InvalidCertificateError(
                f"Certificate an absolute path and a readable file."
            )
        return value

    @root_validator(skip_on_failure=True)
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

    @root_validator(skip_on_failure=True)
    def assign_cert_values(cls, values):
        """Check the certificate."""
        values["session"].headers.update({"X-Skaha-Authentication-Type": "certificate"})
        values["cert"] = values["certificate"]
        values["verify"] = True
        return values

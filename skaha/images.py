"""Skaha Image Management."""

from typing import Dict, List, Optional

from pydantic import model_validator
from requests.models import Response
from typing_extensions import Self

from skaha.client import SkahaClient
from skaha.utils.logs import get_logger

log = get_logger(__name__)


class Images(SkahaClient):
    """Skaha Image Management."""

    @model_validator(mode="after")
    def _set_server(self) -> Self:
        """Sets the server path after validation."""
        self.server = f"{self.server}/{self.version}/image"  # type: ignore
        return self

    def fetch(self, kind: Optional[str] = None) -> List[str]:
        """Get images from Skaha Server.

        Args:
            kind (Optional[str], optional): Type of image. Defaults to None.

        Returns:
            List[str]: A list of images on the skaha server.

        Examples:
            >>> from skaha.images import Images
            >>> images = Images()
            >>> images.fetch(kind="headless")
            ['images.canfar.net/chimefrb/sample:latest',
             ...
             'images.canfar.net/skaha/terminal:1.1.1']
        """
        data: Dict[str, str] = {}
        # If kind is not None, add it to the data dictionary
        if kind:
            data["type"] = kind
        response: Response = self.session.get(url=self.server, params=data)  # type: ignore # noqa
        response.raise_for_status()
        response = response.json()
        reply: List[str] = []
        for image in response:
            reply.append(image["id"])  # type: ignore
        return reply

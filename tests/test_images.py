"""Test Skaha Images API."""

import pytest

from skaha.images import Images


@pytest.fixture(scope="session")
def images():
    """Test images."""
    images = Images()
    yield images
    del images


def test_images_fetch(images):
    """Test fetching images."""
    assert images.fetch()


def test_images_with_kind(images):
    """Test fetching images with kind."""
    assert images.fetch(kind="headless")

"""Data transfer objects."""
# pylint: disable=too-many-instance-attributes
from dataclasses import dataclass


@dataclass
class PostDTO:
    """Encapsulate Mattermost Posts."""
    id: str
    create_at: int
    message: str
    reporter: str
    doi: str

    def __str__(self):
        return self.message


@dataclass
class PaperDTO:
    """Encapsulate Paper meta data."""
    author: str
    authors: str
    title: str
    journal: str
    year: int
    abstract: str
    doi: str
    slug: str

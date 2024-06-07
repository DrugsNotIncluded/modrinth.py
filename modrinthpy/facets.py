from enum import Enum
from typing import Self
from datetime import datetime
from dataclasses import dataclass

@dataclass(frozen=True)
class Facet:
    """
    These are the most commonly used facet types:
    """
    ProjectType = "project_type"
    Categories = "categories"
    Versions = "versions"
    ClientSide = "client_side"
    ServerSide = "server_side"
    OpenSource = "open_source"
    """
    Several others are also available for use, though these should not be used outside very specific use cases:
    """
    Title = "title"
    Author = "author"
    Follows = "follows"
    ProjectID = "project_id"
    License = "license"
    Downloads = "downloads"
    Color = "color"
    CreatedTimestamp = "created_timestamp"
    ModifiedTimestamp = "modified_timestamp"
    def __lt__(a: Self, b: int|str|datetime) -> str:
        return(FacetContainer(a, '<', b))
    def __gt__(a: Self, b: int|str) -> str:
        return(FacetContainer(a, '>', b))
    def __le__(a: Self, b: int|str|datetime) -> str:
        return(FacetContainer(a, '<=', b))
    def __ge__(a: Self, b: int|str) -> str:
        return(FacetContainer(a, '>=', b))
    def __eq__(a: Self, b: int|str|datetime) -> str:
        return(FacetContainer(a, ':', b))


@dataclass
class FacetContainer:
    key: Facet
    sign: str
    value: int|str|datetime
    def get(self):
        return(f'"{self.key}{self.sign}{self.value}"')

def facets_to_str(facets: list[list[FacetContainer]]):
    result = ','.join([f'[{','.join([facet.get() for facet in group])}]' for group in facets])
    return f'[{result}]'
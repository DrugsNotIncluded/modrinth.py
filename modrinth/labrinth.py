import asyncio
from types import SimpleNamespace
from dataclass_wizard import fromdict

from .types import *
from .http.labrinth_http import LabrinthHTTP
from .facets import Facet, facets_to_str
from .endpoints import endpoints


class ModrinthProjects:
    def __init__(self, labrinth_client):
        self.labrinth_client = labrinth_client
        self._api = self.labrinth_client.api

    async def search_project(
        self, 
        query: Optional[str] = None, 
        facets: Optional[str|list[list[Facet]]] = None, 
        index: Optional[SortingMethod] = None, 
        offset: Optional[int] = None,
        limit: Optional[int] = None
        ) -> list[ProjectResult]:
        """
        :param limit: range [0..100]. Default=10
        """
        query_pass = {}
        if query: query_pass['query'] = query
        if not isinstance(facets, str) and facets:
            facets = facets_to_str(facets)
        if facets: query_pass['facets'] = facets
        if index: query_pass['index'] = index
        if offset: query_pass['offset'] = offset
        if limit: query_pass['limit'] = limit
        response = await self._api(endpoints['search_projects'], query=query_pass)
        hits = [fromdict(ProjectResult, project) for project in response['hits']]
        return(hits)

    async def get_project(self, id: str) -> Project:
        """
        :param id: Accepts id or slug.
        """
        response = await self._api(endpoints["get_project"], params={"id":id})
        project = fromdict(Project, response)
        return(project)



class ModrinthClient:
    def __init__(self, labrinth_client: Optional[LabrinthHTTP] = None):
        if not labrinth_client:
            self._labrinth_client = LabrinthHTTP()
        else:
            self._labrinth_client = labrinth_client
        # API parts:
        self._Projects = ModrinthProjects(self._labrinth_client)
    
    @property
    def Projects(self) -> ModrinthProjects:
        return(self._Projects)
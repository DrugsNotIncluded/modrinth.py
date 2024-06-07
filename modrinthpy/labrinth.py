import asyncio
from types import SimpleNamespace
from typing import TypeVar, Generic
from dataclass_wizard import fromdict, asdict
import aiohttp, json
from fnmatch import fnmatch

from .types import *
from .api import LabrinthHTTP
from .facets import Facet, facets_to_str
from .endpoints import endpoints

T = TypeVar('T')

async def tojson(o: bytes):
    return json.loads(await o.read())

def asobj(cls: Generic[T], d: object) -> T:
    """Converts response content to class"""
    return fromdict(cls, d)

def asobj_list(cls: Generic[T], d: object) -> list[T]:
    """Converts response content to list[class]"""
    return [fromdict(cls, t) for t in d]

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
        hits = asobj_list(ProjectResult, (await tojson(response))['hits'])
        return hits

    async def get_project(self, id: str) -> Project:
        """
        :param id: Accepts id or slug.
        """
        response = await self._api(endpoints["get_project"], params={"id":id})
        project = asobj(Project, await tojson(response))
        return project

    async def modify_project(
        self,
        id: str,
        slug: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        categories: Optional[list[str]] = None,
        client_side: Optional[Required] = None,
        server_side: Optional[Required] = None,
        body: Optional[str] = None,
        status: Optional[Status] = None,
        requested_status: Optional[RequestedStatus] = None,
        additional_categories: Optional[list[str]] = None,
        issues_url: Optional[str] = None,
        source_url: Optional[str] = None,
        wiki_url: Optional[str] = None,
        discord_url: Optional[str] = None,
        donation_urls: Optional[ProjectDonationURL] = None,
        license_id: Optional[str] = None,
        license_url: Optional[str] = None
        ):
        data = {}
        if slug: data['slug'] = slug
        if title: data['title'] = title
        if description: data['description'] = description
        if categories: data['categories'] = categories
        if client_side: data['client_side'] = asdict(client_side)
        if server_side: data['server_side'] = asdict(server_side)
        if body: data['body'] = body
        if status: data['status'] = asdict(status)
        if requested_status: data['requested_status'] = asdict(requested_status)
        if additional_categories: data['additional_categories'] = additional_categories
        if issues_url: data['issues_url'] = issues_url
        if source_url: data['source_url'] = source_url
        if wiki_url: data['wiki_url'] = wiki_url
        if discord_url: data['discord_url'] = discord_url
        if donation_urls: data['donation_urls'] = asdict(donation_urls)
        if license_id: data['license_id'] = license_id
        if license_url: data['license_url'] = license_url

        response = await self._api(endpoints["modify_project"], params={"id":id}, json=data)
        return response.read()

    async def delete_project(self, id: str):
        response = await self._api(endpoints["delete_project"], params={"id":id})
        return response.read()

    async def get_multiple_projects(self, ids: list[str]) -> list[Project]:
        """
        :param ids: Accepts ids or slugs.
        """
        ids = f"[{','.join([f'"{id}"' for id in ids])}]"
        response = await self._api(endpoints["get_multiple_projects"], query={"ids":ids})
        projects = asobj_list(Project, await tojson(response))
        return projects

    async def bulk_edit_projects(
        self,
        categories: Optional[list[str]] = None,
        add_categories: Optional[list[str]] = None,
        remove_categories: Optional[list[str]] = None,
        additional_categories: Optional[list[str]] = None,
        add_additional_categories: Optional[list[str]] = None,
        remove_additional_categories: Optional[list[str]] = None,
        donation_urls: Optional[list[str]] = None,
        add_donation_urls: Optional[list[str]] = None,
        remove_donation_urls: Optional[list[str]] = None,
        issues_url: Optional[str] = None,
        source_url: Optional[str] = None,
        wiki_url: Optional[str] = None,
        discord_url: Optional[str] = None
        ):
        data = {}
        if categories: data['categories'] = categories
        if add_categories: data['add_categories'] = add_categories
        if remove_categories: data['remove_categories'] = remove_categories
        if additional_categories: data['additional_categories'] = additional_categories
        if add_additional_categories: data['add_additional_categories'] = add_additional_categories
        if remove_additional_categories: data['remove_additional_categories'] = remove_additional_categories
        if donation_urls: data['donation_urls'] = donation_urls
        if add_donation_urls: data['add_donation_urls'] = add_donation_urls
        if remove_donation_urls: data['remove_donation_urls'] = remove_donation_urls
        if issues_url: data['issues_url'] = issues_url
        if source_url: data['source_url'] = source_url
        if wiki_url: data['wiki_url'] = wiki_url
        if discord_url: data['discord_url'] = discord_url
        response = await self._api(endpoints['bulk_edit_projects'], data=data)

    async def get_random_projects(count: int) -> list[Project]:
        response = self._api(endpoints['get_random_projects'], query={"count":count})
        projects = asobj_list(Project, await tojson(response))
        return projects
    
    async def create_project(
        self,
        slug: str,
        title: str,
        description: str,
        categories: list[str],
        client_side: Required,
        server_side: Required,
        body: str,
        license_id: str,
        project_type: ProjectType,
        status: Optional[Status] = None,
        requested_status: Optional[RequestedStatus] = None,
        additional_categories: Optional[list[str]] = None,
        issues_url: Optional[str] = None,
        source_url: Optional[str] = None,
        wiki_url: Optional[str] = None,
        discord_url: Optional[str] = None,
        donation_urls: Optional[list[ProjectDonationURL]] = None,
        license_url: Optional[str] = None,
        icon: Optional[str|bytearray] = None
    ):
        data = {
            'slug':slug,
            'title':title, 
            'description':description, 
            'categories':categories, 
            'client_side':client_side, 
            'server_side':server_side, 
            'body':body, 
            'license_id':str, 
            'project_type':project_type,
            'is_draft': True,     # DEPRECATED, BUT MUST BE DECLARED
            'initial_versions':[] # DEPRECATED, BUT MUST BE DECLARED
            }
        if status: data['status'] = status
        if requested_status: data['requested_status'] = asdict(requested_status)
        if additional_categories: data['additional_categories'] = additional_categories
        if issues_url: data['issues_url'] = issues_url
        if source_url: data['source_url'] = source_url
        if wiki_url: data['wiki_url'] = wiki_url
        if discord_url: data['discord_url'] = discord_url
        if donation_urls: data['donation_urls'] = donation_urls
        if license_id: data['license_id'] = license_id
        if license_url: data['license_url'] = license_url
        
        with aiohttp.MultipartWriter('form-data') as mp:
            part = mp.append_json(data)
            part.set_content_disposition('form-data', name='data')
            if icon:
                if isinstance(icon, str):
                    with open(icon, 'rb') as icon_file:
                        icon_file.write(icon)
                icon_part = mp.append(icon_file)
                icon_part.set_content_disposition('form-data', name='icon')

            response = await self._api(endpoints['create_project'], data=mp)
        return asobj(Project, tojson(response))

    async def change_project_icon(self, id: str, icon: str|bytearray, extension: Optional[str] = None):
        acceptable_extensions = ["*.png","*.jpg","*.jpeg","*.bmp","*.gif","*.webp","*.svg","*.svgz","*.rgb"]
        # TODO
        matched = [fnmatch(extension, pattern) for pattern in acceptable_extensions]
        print(icon)
        if sum(matched) == 1:
            if isinstance(icon, str):
                    with open(icon, 'rb') as icon_file:
                        icon = icon_file.read()

        await self._api(endpoints['change_project_icon'], data=icon, params={'id':id}, query={"ext":extension[2:]})

    async def delete_project_icon(self, id: str):
        response = await self._api(endpoints['delete_project_icon'], params={'id':id})

    async def check_id_validity(self, id: str) -> str: #id or slug
        response = await self._api(endpoints["check_id_validity"], params={"id":id})
        return await tojson(response)['id']

    async def add_gallery_image(
        self, 
        id: str,
        image: bytearray|str,
        featured: bool = False,
        extension: Optional[str] = None,
        ordering: Optional[int] = None
        ):
        # TODO: No extension extraction from file for now, add manually. Image extensions are the same across all image methods
        # TODO: Add AcceptableImageExtensions class 
        # "check" method will check and return valid exnension if binary data image or passed by name image has one
        if isinstance(image, str):
            with open(image, 'rb') as image_file:
                image = image_file.read()
        query = {
            "featured":json.dumps(featured),
            "ext":extension
            }
        if ordering: query["ordering"] = ordering
        await self._api(endpoints["add_gallery_image"], params={"id":id}, data=image, query=query)

    async def modify_gallery_image(
        self,
        id: str,
        url: str,
        featured: Optional[bool] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        ordering: Optional[int] = None
    ):
        query={"url":url}
        if featured: query["featured"] = json.dumps(featured) # TODO: Remove automatic to json conversion for query in aiohttp client 
        if title: query["title"] = title
        if description: query["description"] = description
        if ordering: query["ordering"] = ordering
        await self._api(endpoints["modify_gallery_image"], query=query, params={'id':id})

    async def delete_gallery_image(self, id: str, url: str):
        await self._api(endpoints["delete_gallery_image"], query={"url":url})
    
    async def get_project_dependencies(self, id:str) -> tuple[list[Project], list[Version]]:
        response = await self._api(endpoints["get_project_dependencies"], params={'id':id})
        response = await tojson(response)
        projects = asobj_list(Project, response['projects'])
        versions = asobj_list(Version, response['versions'])
        return projects, versions

    async def follow_project(self, id:str):
        await self._api(endpoints["follow_project"], params={"id":id})

    async def unfollow_project(self, id:str):
        await self._api(endpoints["unfollow_project"], params={"id":id})

    async def schedule_project(
        self,
        id: str,
        time: datetime,
        requested_status: RequestedStatus
        ):
        await self._api(endpoints["schedule_project"], params={'id':id}, json={"time":time, "requested_status":requested_status})
        

class ModrinthClient:
    def __init__(self, api_key: Optional[str] = None, labrinth_client: Optional[LabrinthHTTP] = None):
        if not labrinth_client:
            if not api_key:
                self._labrinth_client = LabrinthHTTP()
            else:
                self._labrinth_client = LabrinthHTTP(api_key=api_key)
        else:
            self._labrinth_client = labrinth_client
        # API parts:
        self._Projects = ModrinthProjects(self._labrinth_client)
        #self._Versions = ModrinthVersions(self._labrinth_client)

    async def close(self):
       await self._labrinth_client.close()
    
    @property
    def Projects(self) -> ModrinthProjects: return(self._Projects)
""" 
    @property
    def Versions(self) -> ModrinthVersions: return(self._Versions)

    @property
    def VersionFiles(self) -> ModrinthVersionFiles: return(self._VersionFiles)

    @property
    def Users(self) -> ModrinthUsers: return(self._Users)

    @property
    def Notifications(self) -> ModrinthNotifications: return(self._Notifications)

    @property
    def Threads(self) -> ModrinthThreads: return(self._Threads)

    @property
    def Teams(self) -> ModrinthTeams: return(self._Teams)

    @property
    def Tags(self) -> ModrinthTags: return(self._Tags)

    @property
    def Miscellaneous(self) -> ModrinthMiscellaneous: return(self._Miscellaneous) """
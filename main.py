import asyncio
from modrinth.http.labrinth_http import LabrinthHTTP
from modrinth.labrinth import ModrinthClient
from modrinth.types import Project, Required, ProjectType
from modrinth.facets import Facet
from dataclass_wizard import asdict

import aiohttp, json
from aiohttp import FormData
from aiohttp.client import DEFAULT_TIMEOUT


my_test_token ='mrp_nIdEjX5pFjXVBRLJXmIbjn6IC5zPteo3O29KC6utB6u6ugLvWPlHSwq8HtiH'
project_id = 'zL1fFCOd'

async def main():
    try:
        client = ModrinthClient(api_key=my_test_token)
        #client = ModrinthClient()
        #response = await client.Projects.get_multiple_projects(ids=['create','sodium'])

        """ response = await client.Projects.create_project(
            'definitely_not_test',
            'Test',
            'Ayyyooooo, test project creation via API',
            ['decoration','technology'],
            client_side=Required.Required,
            server_side=Required.Optional,
            body='Testssss',
            license_id='MIT',
            project_type=ProjectType.Mod
        ) """

        """ response = await client.Projects.change_project_icon(
            id=project_id,
            icon='test.webp', 
            extension='*.webp')
        """
        #response = await client.Projects.delete_project_icon(project_id)
        #response = await client.Projects.modify_project(project_id, title='Coffee test num2')
        #response = await client.Projects.check_id_validity(project_id)
        #response = await client.Projects.add_gallery_image(project_id, 'test.webp', featured=True, extension='webp')
        print(response)
    finally:
        await client._labrinth_client.close()
    
asyncio.run(main())
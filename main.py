import asyncio, json
from modrinthpy import ModrinthClient

project_id = 'zL1fFCOd'

async def main():
    try:
        #client = ModrinthClient(api_key=my_test_token)
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
        client = ModrinthClient(my_test_token)
        response = await client.Projects.search_project(query='Create')
        print(response)
    finally:
        await client.close()
    
async def test():
    DEFAULT_USERAGENT = "github.com/DrugsNotIncluded/modrinth.py (coffeemeowgirl@gmail.com , t.me/humanised_doll)"
    BASE_API = 'https://api.modrinth.com'
    """ test_endpoint = '/v2/project/create'
    client = AiohttpClient(user_agent=DEFAULT_USERAGENT)
    response = await client.get(test_endpoint)
    print(json.loads(await response.read())) """
    client = ModrinthClient()
    print(await client.Projects.get_project('create'))

asyncio.run(main())
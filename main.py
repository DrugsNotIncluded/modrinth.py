import asyncio
from modrinth.labrinth import ModrinthClient
from modrinth.facets import Facet

async def main():
    client = ModrinthClient()
    #response = await client.Projects.search_project(facets=[[Facet.Versions == '1.7.10'],[Facet.ProjectType == 'mod']])
    response = await client.Projects.get_project('LNytGWDc')
    print(response)
    



asyncio.run(main())
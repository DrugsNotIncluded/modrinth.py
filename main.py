from modrinth.http.aiohttp_client import AiohttpClient
import asyncio
from modrinth.types import GET, POST, DOWNLOAD, endpoint, ProjectResult, Facet
# test
from urllib.parse import quote_plus
from dataclass_wizard import asdict, fromdict

endpoints = {
    "search_projects":endpoint(GET, '/v2/search?facets=[["categories:forge"],["versions:1.7.10"],["project_type:mod"]]')
}

async def main():
    try:
        facets = f'facets={[[Facet.Versions=='1.7.10'], [Facet.ProjectType=="mod"]]}'
        user_agent = "github.com/DrugsNotIncluded/modrinth.py (coffeemeowgirl@gmail.com)"
        client = AiohttpClient(user_agent=user_agent, testing=False)
        #response = await client.get(endpoints["search_projects"].endpoint)
        #hits = [fromdict(ProjectResult, project) for project in response['hits']]
        print(facets)
        #print(hits)
    finally:
        await client.close()

asyncio.run(main())
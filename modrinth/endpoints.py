from .types import endpoint, GET, POST, PUT, PATCH, DEL, DOWNLOAD

endpoints = {
    "search_projects":endpoint(GET, '/v2/search?'),
    "get_project":endpoint(GET, '/v2/project/{id}')
    }
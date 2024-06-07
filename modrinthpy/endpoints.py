from .types import endpoint, GET, POST, PUT, PATCH, DEL, DOWNLOAD

endpoints = {
    "search_projects":endpoint(GET, '/v2/search?'),
    "get_project":endpoint(GET, '/v2/project/{id}'),
    "modify_project":endpoint(PATCH, '/v2/project/{id}'),
    "delete_project":endpoint(DEL, '/v2/project/{id}'),
    "get_multiple_projects":endpoint(GET, '/v2/projects?'),
    "bulk_edit_projects":endpoint(PATCH, '/v2/projects'),
    "create_project":endpoint(POST, '/v2/project'),
    "change_project_icon":endpoint(PATCH, '/v2/project/{id}/icon?'),
    "delete_project_icon":endpoint(DEL, '/v2/project/{id}/icon'),
    "check_id_validity":endpoint(GET, '/v2/project/{id}/check'),
    "add_gallery_image":endpoint(POST, '/v2/project/{id}/gallery?'),
    "modify_gallery_image":endpoint(PATCH, '/v2/project/{id}/gallery?'),
    "delete_gallery_image":endpoint(DEL, '/v2/project/{id}/gallery'),
    "get_project_dependencies":endpoint(GET, '/v2/project/{id}/dependencies'),
    "follow_project":endpoint(POST, '/v2/project/{id}/follow'),
    "unfollow_project":endpoint(DEL, '/v2/project/{id}/follow'),
    "schedule_project":endpoint(POST, '/v2/project/{id}/schedule')
    }
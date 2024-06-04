Maps = {
    "list": {
        "method": "GET",
        "path": "v1/users",
        "query": """{{
            "start_cursor": {start_cursor},
            "page_size": {page_size}
        }}"""
    },
    "get": {
        "method": "GET",
        "path": "v1/users/{user_id}"
    },
    "me": {
        "method": "GET",
        "path": "v1/users/me"
    }
}

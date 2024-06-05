Maps = {
    "get": {
        "method": "GET",
        "path": "v1/databases/{database_id}"
    },
    "filter": {
        "method": "POST",
        "path": "v1/databases/{database_id}/query",
        "payload": """{{
            "filter": {filter}
        }}"""
    }
}

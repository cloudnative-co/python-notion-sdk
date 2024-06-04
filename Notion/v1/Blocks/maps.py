Maps = {
    "get": {
        "method": "GET",
        "path": "v1/blocks/{block_id}"
    },
    "children": {
        "method": "GET",
        "path": "v1/blocks/{block_id}/children",
        "query": """{{
            "start_cursor": {start_cursor},
            "page_size": {page_size}
        }}"""
    },
    "append": {
        "method": "PATCH",
        "path": "v1/blocks/{block_id}/children",
        "payload": """{{
            "children": {children},
            "after": {after}
        }}"""
    },
}

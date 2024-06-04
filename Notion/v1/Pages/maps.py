Maps = {
    "get": {
        "method": "GET",
        "path": "v1/pages/{page_id}",
        "query": """{{
            "filter_properties": {filter_properties}
        }}"""
    },
    "create": {
        "method": "POST",
        "path": "v1/pages",
        "payload": """{{
            "parent": {{
                "database_id": {database_id}
            }},
            "properties": {properties},
            "children": {children},
            "icon": {icon},
            "cover": {cover}
        }}"""
    }
}

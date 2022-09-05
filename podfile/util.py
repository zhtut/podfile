def process_pod_keys(content: dict):
    if isinstance(content, dict):
        new_content = {}
        for key in content:
            new_content[f":{key}"] = content.get(key)
        return new_content
    return content

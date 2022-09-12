def process_pod_keys(content: dict):
    if isinstance(content, dict):
        new_content = {}
        for key in content:
            new_content[f":{key}"] = f":{content.get(key)}"
        return new_content
    return content

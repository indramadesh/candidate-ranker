import json

def load_raw_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def save_json_file(path: str, content):
    # Accept both dict and string
    if isinstance(content, dict):
        data = content
    else:
        data = json.loads(content)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

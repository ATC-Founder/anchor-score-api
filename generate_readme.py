# generate_readme.py
from pathlib import Path


import requests
import json

# Replace this URL if running remotely or behind a tunnel
OPENAPI_URL = "http://127.0.0.1:8000/openapi.json"

response = requests.get(OPENAPI_URL)
spec = response.json()

lines = [f"# 📘 {spec.get('info', {}).get('title', 'API')} Documentation\n"]

# Description and version
desc = spec.get("info", {}).get("description", "")
version = spec.get("info", {}).get("version", "")
lines.append(f"**Version:** {version}\n")
lines.append(f"{desc}\n")

# Iterate over paths
for path, methods in spec.get("paths", {}).items():
    for method, details in methods.items():
        method_upper = method.upper()
        summary = details.get("summary", "")
        description = details.get("description", "")
        lines.append(f"\n## `{method_upper} {path}` — {summary}")
        if description:
            lines.append(f"\n{description}")
        
        # Parameters
        if "parameters" in details:
            lines.append(f"\n### 🔑 Parameters:")
            for param in details["parameters"]:
                name = param["name"]
                location = param["in"]
                required = param.get("required", False)
                param_type = param.get("schema", {}).get("type", "string")
                lines.append(f"- **{name}** ({location}, `{param_type}`){' — Required' if required else ''}")

        # Request Body
        if "requestBody" in details:
            content = details["requestBody"]["content"]
            example = None
            for mime, mime_data in content.items():
                example = mime_data.get("example") or next(iter(mime_data.get("examples", {}).values()), {}).get("value")
                break
            if example:
                lines.append(f"\n### 📦 Example Request Body:\n```json\n{json.dumps(example, indent=2)}\n```")

        # Responses
        if "responses" in details:
            lines.append(f"\n### ✅ Responses:")
            for code, response in details["responses"].items():
                desc = response.get("description", "")
                lines.append(f"- **{code}**: {desc}")

# Save the README
Path("README.md").write_text("\n".join(lines))
print("✅ README.md generated successfully.")

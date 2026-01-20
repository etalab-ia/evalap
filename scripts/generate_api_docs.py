import json
import os
import sys

from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html

# Add the project root to sys.path to allow importing evalap modules
sys.path.append(os.getcwd())

from evalap.api.config import API_PREFIX
from evalap.api.main import app


def generate_docs():
    output_dir = "static"
    os.makedirs(output_dir, exist_ok=True)

    # 1. Generate OpenAPI JSON
    openapi_data = app.openapi()

    # Ensure correct openapi version is set if needed, though app.openapi() usually handles it.

    openapi_path = os.path.join(output_dir, "openapi.json")
    with open(openapi_path, "w") as f:
        json.dump(openapi_data, f, indent=2)
    print(f"Generated {openapi_path}")

    # 2. Generate Swagger UI HTML
    # We point the openapi_url to the static file location relative to the server root
    # When served, it will be at /openapi.json relative to the doc page if we set it up that way,
    # or we can use the API_PREFIX if needed.
    # For static hosting, relative path "openapi.json" is usually best if they are in the same dir.

    # In main.py for prod, we will serve these files.
    # The static files will be served at /api-docs and /redoc.
    # The openapi.json will be served at /openapi.json.
    # So relative path from /api-docs to /openapi.json is just "openapi.json"
    # IF we serve them from the same root or handle routing matches.

    # However, usually Swagger UI fetches the schema.
    # If we browse /api-docs, and schema is at /openapi.json.
    # We should probably use the absolute path from root or ensures it resolves.
    # Let's assume the production app serves openapi.json at `API_PREFIX + "/openapi.json"`.

    openapi_url = API_PREFIX + "/openapi.json"

    swagger_response = get_swagger_ui_html(
        openapi_url=openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )
    # Safely decode the response body if it's bytes-like
    if isinstance(swagger_response.body, (bytes, bytearray, memoryview)):
        swagger_html = bytes(swagger_response.body).decode("utf-8")
    else:
        swagger_html = swagger_response.body

    swagger_path = os.path.join(output_dir, "api_docs.html")
    with open(swagger_path, "w") as f:
        f.write(swagger_html)
    print(f"Generated {swagger_path}")

    # 3. Generate ReDoc HTML
    redoc_response = get_redoc_html(
        openapi_url=openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
    )
    # Safely decode the response body if it's bytes-like
    if isinstance(redoc_response.body, (bytes, bytearray, memoryview)):
        redoc_html = bytes(redoc_response.body).decode("utf-8")
    else:
        redoc_html = redoc_response.body

    redoc_path = os.path.join(output_dir, "redoc.html")
    with open(redoc_path, "w") as f:
        f.write(redoc_html)
    print(f"Generated {redoc_path}")


if __name__ == "__main__":
    generate_docs()

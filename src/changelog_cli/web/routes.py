from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from starlette.requests import Request
import markdown
import os
from pathlib import Path
import importlib.resources as pkg_resources
from changelog_cli.web import templates  # assuming this is your package structure
from fastapi.templating import Jinja2Templates

router = APIRouter()

CHANGELOG_PATH = "CHANGELOG.md"

# Get the absolute path to the templates directory
TEMPLATES_DIR = Path(pkg_resources.files("changelog_cli.web") / "templates")

# Initialize templates with absolute path
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/", response_class=HTMLResponse)
async def render_changelog(request: Request):
    if os.path.exists(CHANGELOG_PATH):
        with open(CHANGELOG_PATH, "r", encoding="utf-8") as file:
            markdown_text = file.read()
            html_content = markdown.markdown(markdown_text)
    else:
        html_content = "<p style='color:red;'>CHANGELOG.md not found!</p>"

    return templates.TemplateResponse(
        "index.html", {"request": request, "content": html_content}
    )

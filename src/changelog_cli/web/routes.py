from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from starlette.requests import Request
import markdown
import os
from changelog_cli.web.config import templates

router = APIRouter()

CHANGELOG_PATH = "CHANGELOG.md"


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

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import markdown
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

CHANGELOG_PATH = "CHANGELOG.md"


@app.get("/", response_class=HTMLResponse)
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

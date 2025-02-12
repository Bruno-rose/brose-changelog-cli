import typer
import uvicorn
from changelog_cli.web.app import app as fastapi_app

app = typer.Typer()


@app.command()
def web(host: str = "127.0.0.1", port: int = 8000):
    """Start the changelog web viewer"""
    uvicorn.run(fastapi_app, host=host, port=port)

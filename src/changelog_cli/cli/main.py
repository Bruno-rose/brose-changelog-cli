import typer
from changelog_cli.cli.commands.generate import generate
from changelog_cli.cli.commands.web import web

app = typer.Typer()

# Add commands directly
app.command()(generate)
app.command()(web)

if __name__ == "__main__":
    app()

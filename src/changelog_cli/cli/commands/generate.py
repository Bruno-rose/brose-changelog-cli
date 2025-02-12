from typing import Optional
import typer
import json
import os
from tqdm import tqdm
from changelog_cli.core.git import get_commit_changes, commits_to_generate_changelogs
from changelog_cli.services.ai_service import generate_changelog
from changelog_cli.services.markdown_service import create_changelog_markdown

app = typer.Typer()


@app.callback()
def callback():
    """Generate changelog entries from commits"""
    pass


@app.command()
def generate():
    """Generate changelog entries from new commits"""
    typer.echo("🔍 Analyzing repository...")

    new_commits = commits_to_generate_changelogs()
    if not new_commits:
        typer.echo("✨ No new commits to process")
        return

    typer.echo(f"📝 Found {len(new_commits)} new commits")

    # Load existing changelog entries if file exists
    existing_entries = {}
    if os.path.exists("changelog/changelog.json"):
        with open("changelog/changelog.json", "r") as f:
            existing_entries = json.load(f)

    changelog_entries = {}
    # Create progress bar for commit processing
    with tqdm(
        total=len(new_commits), desc="Generating changelogs", unit="commit"
    ) as pbar:
        for commit in new_commits:
            commit_info = get_commit_changes([commit])
            changelog = generate_changelog(commit_info)
            if changelog.hash != "error":  # Only add successful entries
                changelog_entries[commit] = changelog.model_dump()
            pbar.update(1)

    # Merge existing entries with new entries
    existing_entries.update(changelog_entries)

    # Create changelog directory if it doesn't exist
    os.makedirs("changelog", exist_ok=True)

    # Update the JSON file with merged entries
    with open("changelog/changelog.json", "w") as f:
        json.dump(existing_entries, f, indent=2)

    # Generate markdown file
    markdown_content = create_changelog_markdown(existing_entries)
    with open("CHANGELOG.md", "w") as f:
        f.write(markdown_content)

    typer.echo("✨ Changelog generated successfully!")

import typer
from services.commit_service import (
    get_all_main_branch_commits,
    get_commit_changes,
    get_commit_hashes_from_json,
)
from clients.open_ai_client import generate_changelog
import json
import os

app = typer.Typer()


@app.command()
def generate():
    print("Generating changelog...")
    new_commmits_changes = get_commit_changes()
    new_commmits_hashes = get_all_main_branch_commits()
    old_commmits = get_commit_hashes_from_json()

    commits_to_generate_changelog = [
        commit for commit in new_commmits_hashes if commit not in old_commmits
    ]
    print(f"Found {len(commits_to_generate_changelog)} new commits to process")

    # Generate changelogs and save to JSON
    changelog_entries = {}
    for commit in commits_to_generate_changelog:
        commit_info = get_commit_changes([commit])
        changelog = generate_changelog(commit_info)
        # Convert Pydantic model to dict before storing
        changelog_entries[commit] = changelog.model_dump()

    # Create changelog directory if it doesn't exist
    os.makedirs("changelog", exist_ok=True)

    # Update the JSON file with new entries
    with open("changelog/changelog.json", "w") as f:
        json.dump(changelog_entries, f, indent=2)


@app.command()
def readme():
    print("Generating README...")

    # Read the changelog entries from JSON
    try:
        with open("changelog/changelog.json", "r") as f:
            changelog_entries = json.load(f)
    except FileNotFoundError:
        print(
            "No changelog/changelog.json file found. Please run 'generate' command first."
        )
        return

    if not changelog_entries:
        print(
            "No changelog entries found. Please run 'generate' command to create some entries."
        )
        return

    # Create markdown content with header
    markdown_content = """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

"""

    # Add Unreleased section
    markdown_content += "## [Unreleased]\n\n"

    # Group changes by type
    changes_by_type = {}
    for commit_hash, entry in changelog_entries.items():
        change_type = entry.get("type", "Other")
        if change_type not in changes_by_type:
            changes_by_type[change_type] = []
        changes_by_type[change_type].append({"hash": commit_hash, "entry": entry})

    # Generate markdown sections by type
    for change_type, entries in sorted(changes_by_type.items()):
        if entries:  # Only add sections that have entries
            # print(entries)
            markdown_content += f"### {change_type}\n\n"
            for entry_data in entries:
                entry = entry_data["entry"]
                description = entry.get("message", "")

                changes = entry.get("changes", {})

                added = changes.get("Added", [])
                fixed = changes.get("Fixed", [])
                changed = changes.get("Changed", [])
                removed = changes.get("Removed", [])

                added_text = f"**Added:** {', '.join(added)}\n" if added else ""
                fixed_text = f"**Fixed:** {', '.join(fixed)}\n" if fixed else ""
                changed_text = f"**Changed:** {', '.join(changed)}\n" if changed else ""
                removed_text = f"**Removed:** {', '.join(removed)}\n" if removed else ""

                markdown_content += (
                    f"- {added_text}{fixed_text}{changed_text}{removed_text}\n"
                )

            markdown_content += "\n"

    # Add version comparison links section
    markdown_content += (
        "[unreleased]: https://github.com/owner/repo/compare/v1.0.0...HEAD\n"
    )

    # Write to CHANGELOG.md
    with open("CHANGELOG.md", "w") as f:
        f.write(markdown_content)

    print("CHANGELOG.md has been generated successfully!")


@app.command()
def release(version: str):
    """
    Create a new release version. Example usage:
    - For major: release 2.0.0
    - For minor: release 1.1.0
    - For patch: release 1.0.1
    """
    print(f"Creating release version {version}...")

    # Validate version format
    if not version.replace(".", "").isdigit() or len(version.split(".")) != 3:
        print("Invalid version format. Please use semantic versioning (e.g., 1.0.0)")
        return

    try:
        with open("CHANGELOG.md", "r") as f:
            content = f.read()
    except FileNotFoundError:
        print("CHANGELOG.md not found. Please run 'readme' command first.")
        return

    # Get current date for the release
    from datetime import datetime

    release_date = datetime.now().strftime("%Y-%m-%d")

    # Replace [Unreleased] with the new version
    new_content = content.replace(
        "## [Unreleased]", f"## [Unreleased]\n\n## [{version}] - {release_date}"
    )

    # Update the version links at the bottom
    if "[unreleased]:" in new_content:
        link_section = new_content.split("[unreleased]:")[1]
        new_links = (
            f"[unreleased]: https://github.com/owner/repo/compare/v{version}...HEAD\n"
        )
        new_links += f"[{version}]: https://github.com/owner/repo/compare/v{get_previous_version(content)}...v{version}\n"
        new_content = new_content.split("[unreleased]:")[0] + new_links

    # Write the updated content
    with open("CHANGELOG.md", "w") as f:
        f.write(new_content)

    print(f"Release {version} has been created successfully!")


def get_previous_version(content: str) -> str:
    """Extract the previous version from the changelog content."""
    import re

    versions = re.findall(r"## \[(\d+\.\d+\.\d+)\]", content)
    return versions[0] if versions else "0.0.0"


if __name__ == "__main__":
    app()

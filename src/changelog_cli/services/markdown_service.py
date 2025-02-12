from datetime import datetime, timedelta


def create_changelog_markdown(changelog_entries: dict) -> str:
    """
    Create a markdown formatted changelog from changelog entries.

    Args:
        changelog_entries (dict): Dictionary of commit hashes and their changelog entries

    Returns:
        str: Formatted markdown content
    """
    markdown_content = create_markdown_header()
    markdown_content += format_entries_by_type(changelog_entries)
    return markdown_content


def create_markdown_header() -> str:
    """Create the standard header for the changelog markdown"""
    return """# Changelog 📝

All notable changes to this project will be documented on this site.

---
"""


def format_entries_by_type(entries: dict) -> str:
    """Format entries grouped by week and then by commit"""
    # Group changes by week
    changes_by_week = {}
    for commit_hash, entry in entries.items():
        # Skip version_map and error entries
        if commit_hash == "version_map" or entry.get("hash") == "error":
            continue

        # Parse the date string to datetime
        date_str = entry.get("date", "")
        try:
            date = datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y %z")
            # Format week as "Week of Month Day, Year"
            week_start = date - timedelta(days=date.weekday())
            week_key = week_start.strftime("Week of %B %d, %Y")

            if week_key not in changes_by_week:
                changes_by_week[week_key] = []
            changes_by_week[week_key].append(entry)
        except ValueError:
            # Handle invalid date format
            if "Unknown Week" not in changes_by_week:
                changes_by_week["Unknown Week"] = []
            changes_by_week["Unknown Week"].append(entry)

    content = ""
    # Add each week section
    for week in sorted(changes_by_week.keys(), reverse=True):
        week_entries = sorted(
            changes_by_week[week],
            key=lambda x: (
                datetime.strptime(x.get("date", ""), "%a %b %d %H:%M:%S %Y %z")
                if x.get("date")
                else datetime.min
            ),
            reverse=True,
        )

        # Filter week_entries to only include those with high relevance changes
        week_entries = [
            entry
            for entry in week_entries
            if any(
                change.get("relevance_score", 0) >= 6
                for category in ["Added", "Fixed", "Changed", "Removed"]
                for change in entry.get("changes", {}).get(category, [])
            )
        ]

        # Skip week if no relevant entries
        if not week_entries:
            continue

        content += f"## 📅 {week}\n\n"

        # Add each commit
        for entry in week_entries:
            commit_message = entry.get("message", "No message")
            content += f"### 🔖 {commit_message}\n\n"

            # Add date and time in a subtle format
            if entry.get("date"):
                try:
                    date = datetime.strptime(
                        entry.get("date"), "%a %b %d %H:%M:%S %Y %z"
                    )
                    content += f"*{date.strftime('%B %d, %Y at %I:%M %p')}*\n\n"
                except ValueError:
                    pass

            # Category icons mapping
            category_icons = {
                "Added": "✨",
                "Fixed": "🔧",
                "Changed": "📝",
                "Removed": "🗑️",
            }

            for category in ["Added", "Fixed", "Changed", "Removed"]:
                changes = entry.get("changes", {}).get(category, [])
                # Filter changes to only include those with relevance >= 6
                relevant_changes = [
                    c for c in changes if c.get("relevance_score", 0) >= 6
                ]

                if relevant_changes:
                    icon = category_icons.get(category, "")
                    content += f"#### {icon} {category}\n\n"
                    # Sort changes by relevance score in descending order
                    sorted_changes = sorted(
                        relevant_changes,
                        key=lambda x: x.get("relevance_score", 0),
                        reverse=True,
                    )
                    for change in sorted_changes:
                        description = change.get("description", "")
                        score = change.get("relevance_score", 0)
                        # Add a visual indicator for high-relevance changes (score >= 7)
                        importance_marker = "🔥 " if score >= 7 else ""
                        content += f"- {importance_marker}{description}\n"
                    content += "\n"

            # Add a subtle separator between commits
            content += "---\n\n"

    return content

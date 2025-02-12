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
        if commit_hash == "version_map":
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
        content += f"## 📅 {week}\n\n"

        # Sort entries within week by date
        week_entries = sorted(
            changes_by_week[week],
            key=lambda x: (
                datetime.strptime(x.get("date", ""), "%a %b %d %H:%M:%S %Y %z")
                if x.get("date")
                else datetime.min
            ),
            reverse=True,
        )

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
                if changes:
                    icon = category_icons.get(category, "")
                    content += f"#### {icon} {category}\n\n"
                    for change in changes:
                        content += f"- {change}\n"
                    content += "\n"

            # Add a subtle separator between commits
            content += "---\n\n"

    return content

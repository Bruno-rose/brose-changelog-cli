import subprocess


def get_commit_changes(commit_hashes=None):
    # Git command to get commit history with changes and 50-line context
    git_command = [
        "git",
        "log",
        "-p",
        "-U50",
        "--no-renames",
        "--pretty=format:commit %H%nAuthor: %an%nDate: %ad%n%n%s%n",
    ]

    # Add specific commits if provided
    if commit_hashes:
        git_command.extend(commit_hashes)

    # Run the command and capture the output
    result = subprocess.run(
        git_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        return result.stdout


def get_commit_hashes_from_json(json_file_path="changelog/commits.json"):
    """
    Extract commit hashes from the commits.json file

    Args:
        json_file_path (str): Path to the JSON file containing commit information

    Returns:
        list: List of commit hashes
    """
    import json

    try:
        with open(json_file_path, "r") as file:
            data = json.load(file)
            return [commit["hash"] for commit in data.get("commits", [])]
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_file_path}")
        return []
    except json.JSONDecodeError:
        print("Error: Invalid JSON format")
        return []


def get_all_main_branch_commits():
    """
    Get all commit hashes from the main branch

    Returns:
        list: List of commit hashes from the main branch
    """
    git_command = ["git", "log", "main", "--pretty=format:%H"]

    result = subprocess.run(
        git_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return []

    # Split the output into individual commit hashes
    commit_hashes = result.stdout.strip().split("\n")
    return commit_hashes


# Example usage with specific commits
commit_hashes = [
    "f2111cf5db9369b883609f66cfe09afaab522dad"
]  # Replace with actual commit hashes
commit_changes = get_commit_changes(commit_hashes)
print(commit_changes)

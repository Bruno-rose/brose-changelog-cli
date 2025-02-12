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

    # Add exclude patterns after the commit hashes
    git_command.extend(
        [
            "--",  # Separator between commits and pathspecs
            ":(exclude)*.md",
            ":(exclude)*.lock",
            ":(exclude)*.config.js",
            ":(exclude)*.json",
            ":(exclude)*.yml",
            ":(exclude)*.yaml",
            ":(exclude)Dockerfile",
            ":(exclude).env*",
            ":(exclude).github/**",
            ":(exclude).husky/**",
            ":(exclude)docs/**",
            ":(exclude)tests/**",
            ":(exclude)__tests__/**",
            ":(exclude)*.test.*",
            ":(exclude)*.spec.*",
            ":(exclude)dist/**",
            ":(exclude)build/**",
            ":(exclude)node_modules/**",
            ":(exclude)vendor/**",
            ":(exclude)*.png",
            ":(exclude)*.jpg",
            ":(exclude)*.jpeg",
            ":(exclude)*.gif",
            ":(exclude)*.svg",
            ":(exclude)*.ico",
            ":(exclude)*.pdf",
            ":(exclude)*.xlsx",
            ":(exclude)*.csv",
        ]
    )

    # Run the command and capture the output
    try:
        result = subprocess.run(
            git_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return None
        return result.stdout
    except Exception as e:
        print(f"Error executing git command: {e}")
        return None


def get_commit_hashes_from_json(json_file_path="changelog/changelog.json"):
    """
    Extract commit hashes from the changelog.json file

    Args:
        json_file_path (str): Path to the JSON file containing commit information

    Returns:
        list: List of commit hashes
    """
    import json

    try:
        with open(json_file_path, "r") as file:
            data = json.load(file)
            return list(data.keys())
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


def commits_to_generate_changelogs():
    """
    Get all new commits from the main branch

    Returns:
        list: List of new commit hashes from the main branch
    """

    new_commmits_hashes = get_all_main_branch_commits()
    old_commmits_hashes = get_commit_hashes_from_json()

    return [
        commit for commit in new_commmits_hashes if commit not in old_commmits_hashes
    ]


if __name__ == "__main__":
    commit_hashes = [
        "f2111cf5db9369b883609f66cfe09afaab522dad",
    ]
    commit_changes = get_commit_changes(commit_hashes)
    print(commit_changes)

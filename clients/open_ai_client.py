from typing import Dict, List, Optional
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")


class CommitChanges(BaseModel):
    Added: Optional[List[str]] = []
    Fixed: Optional[List[str]] = []
    Changed: Optional[List[str]] = []
    Removed: Optional[List[str]] = []


class Commit(BaseModel):
    hash: str
    author: str
    date: str
    message: str
    changes: CommitChanges


def generate_changelog(commit_info: str) -> Commit:
    """
    Generate a structured changelog entry using OpenAI API

    Args:
        commit_info (str): Git commit information including message and diff

    Returns:
        Commit: Structured commit information with categorized changes
    """
    prompt = f"""
    Analyze this git commit and categorize the changes into Added, Fixed, Changed, or Removed.
    Return only a JSON object following this structure:
    {{
        "hash": "commit hash",
        "author": "author name",
        "date": "commit date",
        "message": "commit message",
        "changes": {{
            "Added": ["list of additions"],
            "Fixed": ["list of fixes"],
            "Changed": ["list of changes"],
            "Removed": ["list of removals"]
        }}
    }}

    Git commit information:
    {commit_info}
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that analyzes git commits and generates structured changelog entries.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )

    # Parse the response into our Pydantic model
    try:
        commit_data = response.choices[0].message.content
        return Commit.model_validate_json(commit_data)
    except Exception as e:
        print(f"Error parsing OpenAI response: {e}")
        # Return a default commit object in case of error
        return Commit(
            hash="error",
            author="unknown",
            date="unknown",
            message="Error generating changelog",
            changes=CommitChanges(),
        )

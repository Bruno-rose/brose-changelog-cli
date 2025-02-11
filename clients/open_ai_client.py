from typing import Dict, List, Optional
from pydantic import BaseModel
import openai
import os
import json
from dotenv import load_dotenv
from services.commit_service import get_commit_changes

load_dotenv()

# Configure OpenAI API
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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
    print("Generating changelog for commit:", commit_info)
    print("commit info token length:", len(commit_info))
    # Verify API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is not set")
        return Commit(
            hash="error",
            author="unknown",
            date="unknown",
            message="OpenAI API key not configured",
            changes=CommitChanges(),
        )

    try:
        prompt = f"""
        Analyze this git commit and categorize the changes into Added, Fixed, Changed, or Removed.
        Consider the context from the git diff to provide clear, user-friendly descriptions.
        
        Guidelines:
        - Include file paths when relevant
        - Describe the actual change, not just the technical modification
        - Group related changes together
        - Use clear, non-technical language where possible
        - For bug fixes, explain what was fixed rather than just stating "fixed bug"
        
        Return only a JSON object following this structure:
        {{
            "hash": "commit hash",
            "author": "author name",
            "date": "commit date",
            "message": "commit message",
            "changes": {{
                "Added": ["list of user-friendly additions"],
                "Fixed": ["list of user-friendly fixes"],
                "Changed": ["list of user-friendly changes"],
                "Removed": ["list of user-friendly removals"]
            }}
        }}

        Git commit information:
        {commit_info}
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that analyzes git commits and generates structured changelog entries.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            # use response format
        )

        # Add debug logging
        raw_content = response.choices[0].message.content
        print("Raw API response:", raw_content)

        # Strip any potential whitespace and handle markdown code blocks
        cleaned_content = raw_content.strip()
        if cleaned_content.startswith("```json"):
            cleaned_content = cleaned_content[7:]  # Remove ```json prefix
        if cleaned_content.endswith("```"):
            cleaned_content = cleaned_content[:-3]  # Remove ``` suffix
        cleaned_content = cleaned_content.strip()

        commit_data = json.loads(cleaned_content)
        return Commit.model_validate(commit_data)
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Received content: {raw_content}")
        return Commit(
            hash="error",
            author="unknown",
            date="unknown",
            message="Invalid JSON response from API",
            changes=CommitChanges(),
        )
    except openai.RateLimitError as e:
        print(f"OpenAI API Rate Limit Error: {e}")
        return Commit(
            hash="error",
            author="unknown",
            date="unknown",
            message="OpenAI API rate limit exceeded",
            changes=CommitChanges(),
        )
    except Exception as e:
        print(f"Error generating changelog: {e}")
        return Commit(
            hash="error",
            author="unknown",
            date="unknown",
            message="Error generating changelog",
            changes=CommitChanges(),
        )


if __name__ == "__main__":
    commit_info = get_commit_changes(["fdb446aa58edc682945f8d0a801dca2d8ea92725"])
    print("commit_info token length:", len(commit_info))
    print(generate_changelog(commit_info))

from typing import List, Optional

from pydantic import BaseModel
import openai
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Configure OpenAI API
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class Change(BaseModel):
    description: str
    relevance_score: int


class CommitChanges(BaseModel):
    Added: Optional[List[Change]] = []
    Fixed: Optional[List[Change]] = []
    Changed: Optional[List[Change]] = []
    Removed: Optional[List[Change]] = []


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
    # Verify API key is set
    if not os.getenv("OPENAI_API_KEY"):
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
        - For each change, assign a relevance score (1-10) based on how important it is for end-users:
          * 10: Critical functionality or security-related changes
          * 7-9: Major features or significant improvements
          * 4-6: Minor features or quality-of-life improvements
          * 1-3: Technical changes with minimal user impact
        
        Return only a JSON object following this structure:
        {{
            "hash": "commit hash",
            "author": "author name",
            "date": "commit date",
            "message": "commit message",
            "changes": {{
                "Added": [
                    {{"description": "user-friendly description", "relevance_score": number}}
                ],
                "Fixed": [
                    {{"description": "user-friendly description", "relevance_score": number}}
                ],
                "Changed": [
                    {{"description": "user-friendly description", "relevance_score": number}}
                ],
                "Removed": [
                    {{"description": "user-friendly description", "relevance_score": number}}
                ]
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
        )

        raw_content = response.choices[0].message.content
        cleaned_content = raw_content.strip()
        if cleaned_content.startswith("```json"):
            cleaned_content = cleaned_content[7:]
        if cleaned_content.endswith("```"):
            cleaned_content = cleaned_content[:-3]
        cleaned_content = cleaned_content.strip()

        commit_data = json.loads(cleaned_content)
        return Commit.model_validate(commit_data)
    except json.JSONDecodeError:
        print(f"Invalid JSON response from API: {cleaned_content}")
        return Commit(
            hash="error",
            author="unknown",
            date="unknown",
            message="Invalid JSON response from API",
            changes=CommitChanges(),
        )
    except openai.RateLimitError:
        return Commit(
            hash="error",
            author="unknown",
            date="unknown",
            message="OpenAI API rate limit exceeded",
            changes=CommitChanges(),
        )
    except Exception as e:
        return Commit(
            hash="error",
            author="unknown",
            date="unknown",
            message=f"Error generating changelog: {str(e)}",
            changes=CommitChanges(),
        )

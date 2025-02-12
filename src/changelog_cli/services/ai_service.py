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

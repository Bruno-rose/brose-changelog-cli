# brose-changelog-cli

[![PyPI version](https://badge.fury.io/py/brose-changelog-cli.svg)](https://pypi.org/project/brose-changelog-cli/)

An AI-powered changelog generator that creates structured, user-friendly changelogs from your git history.

## Features

- 🤖 AI-powered analysis of git commits
- 📝 Structured changelog generation
- 🌐 Web viewer for changelogs
- 🔍 Smart filtering of relevant changes
- 🎯 Relevance scoring for changes
- 🚫 Automatic exclusion of non-essential files

## Installation

Install from [PyPI](https://pypi.org/project/brose-changelog-cli/) using pip:
```bash
pip install brose-changelog-cli
```

Or with uv:
```bash
uv install brose-changelog-cli
```

## Usage

### Generate Changelog

Create or update your changelog based on new git commits:

```bash
changelog generate
```

This will:
- Analyze new commits in your repository
- Generate structured changelog entries
- Create/update `changelog/changelog.json`
- Generate a formatted `CHANGELOG.md`

### Web Viewer

Launch a web interface to view your changelog:

```bash
changelog web
```

By default, the web viewer runs at `http://127.0.0.1:8000`. You can customize the host and port:

```bash
changelog web --host 0.0.0.0 --port 3000
```

## Configuration

1. Create a `.env` file:
```
OPENAI_API_KEY=your-api-key
```

2. Optionally, set up your OpenAI API key:
```bash
export OPENAI_API_KEY=your-api-key
```


## How It Works

1. **Commit Analysis**: The tool analyzes your git commits, excluding non-essential files like documentation, tests, and configuration files.

2. **AI Processing**: Each commit is processed through OpenAI's GPT model to:
   - Categorize changes (Added, Fixed, Changed, Removed)
   - Generate user-friendly descriptions
   - Assign relevance scores (1-10)

3. **Changelog Generation**: Changes are organized by:
   - Week
   - Commit
   - Change category
   - Relevance (prioritizing high-impact changes)

## Requirements

- Python ≥ 3.12
- Git repository
- OpenAI API key

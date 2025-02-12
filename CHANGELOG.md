# Changelog 📝

All notable changes to this project will be documented on this site.

---
## 📅 Week of February 10, 2025

### 🔖 chore: update gitignore

*February 11, 2025 at 05:38 PM*

#### ✨ Added

- Added entries for version.json in .gitignore

#### 🗑️ Removed

- Removed the *.json line from .gitignore

---

### 🔖 feat: add generate readme and release command

*February 11, 2025 at 10:27 AM*

#### ✨ Added

- Command to generate changelog entries from commits
- Command to generate README file

---

### 🔖 feat: add error handling on openai client

*February 11, 2025 at 10:24 AM*

#### ✨ Added

- Imported json module in open_ai_client.py

#### 📝 Changed

- Replaced openai.api_key assignment with openai.OpenAI initialization in open_ai_client.py

---

### 🔖 feat: add markdown viewer

*February 11, 2025 at 10:23 AM*

#### ✨ Added

- Created markdown_viewer.py for rendering CHANGELOG.md in HTML format
- Added templates folder with index.html for displaying rendered markdown content

---

### 🔖 chore: update dependencies

*February 11, 2025 at 10:22 AM*

#### ✨ Added

- Dependencies: fastapi, jinja2, markdown, python-multipart, uvicorn

---

### 🔖 feat: exclude chore files

*February 11, 2025 at 10:21 AM*

#### 🗑️ Removed

- Excluded various file types and directories like markdown files, lock files, configuration files, JSON files, YAML files, Dockerfile, environment files, GitHub-related files, Husky configuration files, documentation files, test files, image files (png, jpg, jpeg, gif, svg, ico), PDF files, and spreadsheet files (xlsx, csv).

---

## 📅 Week of February 03, 2025

### 🔖 feat: add git commit service

*February 07, 2025 at 04:37 PM*

#### ✨ Added

- Created a new file 'commit_service.py' in the 'services' directory

---

### 🔖 feat: add open ai client

*February 07, 2025 at 04:37 PM*

#### ✨ Added

- Created a new file clients/open_ai_client.py to handle interactions with OpenAI API
- Imported necessary modules for OpenAI interaction
- Configured OpenAI API with the provided API key

---

### 🔖 feat: add open ai client

*February 07, 2025 at 04:37 PM*

#### ✨ Added

- Added OpenAI client implementation
- Added configuration for OpenAI API key

---

### 🔖 initial commit

*February 05, 2025 at 02:25 PM*

#### ✨ Added

- Ignored Python-generated files and virtual environments in .gitignore
- Added .python-version file with Python version 3.12
- Created main.py with commands for saying hello and goodbye
- Added pyproject.toml with project metadata and dependencies

---


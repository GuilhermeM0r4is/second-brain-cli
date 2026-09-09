# Second Brain CLI

> A modular, privacy-focused terminal-based personal knowledge management and study assistant built with Python.

**Second Brain CLI (SBRAIN)** is a terminal application designed to help students organize knowledge, manage notes and study material, process documents, and use AI to transform stored information into useful study resources.

The project was developed as a practical software-engineering and portfolio project, focusing on modular architecture, persistent storage, terminal interfaces, document processing, OCR, AI integration, and clean separation of responsibilities.

---

## Features

### Knowledge Management

* Create, list, search, update, and delete notes
* Search notes by ID, title, or tag
* Manage tags
* Mark notes as favorites
* View note and system statistics
* Responsive note-card interface
* Persistent SQLite storage

### Study System

* Generate AI summaries from notes
* Generate flashcards
* Generate quizzes
* List and search generated study material
* Update and delete flashcards and quizzes
* Store quizzes together with their questions, answers, and explanations
* Structured AI responses with validation and safe parsing

### Document Processing

* Import PDF documents
* Import PowerPoint (`.pptx`) presentations
* Import Markdown/text documents
* Extract document text
* OCR scanned and image-based documents
* Configurable OCR resolution
* Configurable OCR languages
* Split large documents into chunks
* Process document chunks through the AI layer
* Automatically convert imported documents into notes

### AI Integration

SBRAIN uses a provider-independent AI architecture.

Supported providers include:

* Ollama
* OpenAI
* Anthropic
* Google Gemini
* Ollama Cloud

The AI layer is separated from the rest of the application, allowing different providers and models to be configured without coupling the core knowledge-management system to a specific service.

### Terminal Interface

SBRAIN uses a combination of **Rich** and **prompt_toolkit** to provide an interactive terminal experience.

The interface includes:

* Interactive input
* Command autocompletion
* Hierarchical command suggestions
* Usage hints
* Command descriptions
* Responsive note cards
* Rich terminal formatting
* Runtime configuration information
* Terminal-width-aware layouts
* Autocompletions driven by command tree

---

## Privacy

Privacy is an important design goal of SBRAIN.
The application supports **local AI processing through Ollama**, allowing users to process their notes and documents without sending their data to a cloud provider.
Cloud AI providers are optional and require the user to configure their own credentials.

SBRAIN does not require:
* A central SBRAIN server
* A SBRAIN account
* A mandatory cloud AI provider

> When working with sensitive or private study material, local AI models are recommended.

API keys should never be committed to Git.

---

## Requirements

### Software
* Python 3.10+
* Git
* Tesseract OCR — only required for OCR functionality
* Ollama — only required when using local Ollama models

### Python Dependencies
The project separates dependencies into different requirement files:
```text
requirements/
├── requirements.txt
├── requirements-base.txt
├── requirements-ai.txt
└── requirements-ocr.txt
```

The main requirements file combines the base, AI, and OCR dependencies.
Install all dependencies with:
```bash
pip install -r requirements/requirements.txt
```

The base environment includes:
* Rich
* prompt_toolkit
* PyMuPDF
* python-pptx
* Ollama

AI providers add:
* OpenAI
* Anthropic
* Google Gemini

OCR adds:
* pytesseract
* Pillow

---

## Tesseract OCR

SBRAIN uses **Tesseract OCR** for scanned and image-based documents.
Tesseract is a system dependency and must be installed separately from the Python packages.

### Windows

Install Tesseract OCR and make sure the executable is available to SBRAIN.
A typical installation path is:
```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

### Linux
```bash
sudo apt install tesseract-ocr
```

### macOS
```bash
brew install tesseract
```

Verify the installation:
```bash
tesseract --version
```

SBRAIN also allows OCR configuration through its command interface.

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/GuilhermeM0r4is/second-brain-cli.git
cd second-brain-cli
```

### 2. Create a virtual environment

#### Windows
```powershell
python -m venv venv
venv\Scripts\activate
```

#### Linux/macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements/requirements.txt
```

### 4. Optional: install Ollama

Ollama is only required when using local AI models.
After installing Ollama, download a compatible model, for example:

```bash
ollama pull qwen3:1.7b
```

### 5. Optional: install Tesseract
Follow the Tesseract instructions above if OCR functionality is required.

---

## Running SBRAIN
From the project root:
```bash
python run.py
```

The application initializes its SQLite database automatically and launches the interactive terminal interface.
The main prompt uses `/` commands:
```text
SBRAIN > /
```

Typing `/` activates command suggestions and autocomplete.
Just press TAB at any time to look for autocompletions.
Use:
```text
/help
```

to display the complete command documentation.

---

## Commands

### Notes
```text
/note create <title> <content> [tags] [favorite]
/note list
/note find <id/title>
/note find tag <tag>
/note delete <id/title>
/note update <id/title> <new_title> [content] [tags] [favorite]
```

Examples:
```text
/note create Algorithms QuickSort algorithms 1
/note list
/note find 8
/note find tag biology
/note delete My Note
/note update 9 New Title Updated Content algorithms 1
```

The favorite flag accepts:
```text
0 = not favorite
1 = favorite
```

---

### Statistics
```text
/stats
```

Displays information such as:
* Total notes
* Favorite notes
* Most-used tag

---

### Document Import
```text
/import <document> [tags] [favorite]
```

Supported document types include:
* PDF
* PowerPoint
* Markdown/text documents

Imported documents can be extracted, OCR-processed when necessary, chunked, processed through the AI layer, and converted into notes.

---

### Study Material
```text
/study list <type>
/study find <type> <id/title>
/study delete <type> <id/title>
/study update <type> <id/title> ...
/study sum <id/title>
/study cards <id/title>
/study quiz <id/title>
/study all <id/title>
```

Supported study material types:
```text
cards
quiz
```

Examples:
```text
/study find cards biology
/study delete cards 9
/study update cards 9 New Title New Front New Back
/study sum 9
/study cards Biology
/study quiz Biology
/study all 9
```

`/study all` can be used to generate the available study resources for a note.

---

### Configuration
```text
/config dpi <value>
/config language <language>
/config ai provider:<provider> | api_key:<key> | model:<model>
```

Examples:
```text
/config dpi 300
/config language eng+por
/config ai provider:ollama | model:qwen3:1.7b
```

The AI configuration supports:
```text
ollama
openai
anthropic
gemini
```

---

### Help
```text
/help
```

Help is hierarchical and can provide information about individual commands and subcommands.

For example:
```text
/help note
/help note create
/help study
/help config ai
```

The same command structure is also used by the autocomplete system.

---

## Architecture
SBRAIN is organized into separate application layers.

```text
Second-Brain-cli/
│
├── run.py
│
├── application/
│   ├── main.py
│   │
│   ├── documents/
│   │   ├── documents.py
│   │   ├── model.py
│   │   ├── ocr.py
│   │   ├── pdf.py
│   │   ├── pptx.py
│   │   └── text.py
│   │
│   ├── material/
│   │   ├── config.py
│   │   ├── formatting.py
│   │   ├── material.py
│   │   ├── model.py
│   │   └── note.py
│   │
│   ├── storage/
│   │   ├── configure.py
│   │   ├── db.py
│   │   ├── schema.sql
│   │   └── storage.py
│   │
│   └── study/
│       ├── communication.py
│       ├── config.py
│       ├── formatting.py
│       ├── model.py
│       ├── parsing.py
│       ├── prompting.py
│       ├── safe_guarding.py
│       └── study.py
│
├── ui/
│   ├── completer.py
│   ├── header.py
│   ├── helper.py
│   ├── input.py
│   └── listing.py
│
├── requirements/
│   ├── requirements.txt
│   ├── requirements-base.txt
│   ├── requirements-ai.txt
│   └── requirements-ocr.txt
│
├── .gitignore
└── README.md
```

### `application/`
Contains the core application logic.

### `application/material/`
Handles the primary knowledge-management system, including notes, tags, favorites, searching, updating, deletion, formatting, and statistics.

### `application/study/`
Handles AI-generated study material, including summaries, flashcards, quizzes, structured responses, parsing, prompting, and safety validation.

### `application/documents/`
Handles document import and processing, including PDF, PowerPoint, text extraction, and OCR.

### `application/storage/`
Contains the SQLite persistence layer, database initialization, configuration, schema, and data-access operations.

### `ui/`
Contains the terminal presentation and interaction layer.
The UI is intentionally separated from the core application logic and provides:

* Rich rendering
* Interactive input
* Autocomplete
* Command help
* Note-card layouts
* Runtime settings display

### `run.py`
The application entry point.

---

## Data Storage
SBRAIN uses **SQLite** for persistent local storage.
The database contains dedicated structures for:

* Application settings
* Notes
* Tags
* Note/tag relationships
* Flashcards
* Quizzes
* Quiz questions

The database schema uses relational tables and foreign-key relationships to keep notes, tags, and generated study material organized.
All application data is stored locally on the user's machine.

---

## Document Processing Pipeline
SBRAIN's document workflow is designed around transforming external study material into usable knowledge.
```text
Document
   ↓
Import
   ↓
Text Extraction / OCR
   ↓
Chunking
   ↓
AI Processing
   ↓
Automatic Note Creation
   ↓
SQLite Storage
```

This allows large documents to be processed incrementally rather than requiring the entire document to be sent to an AI model in a single request.

---

## AI Safety and Validation
AI output is not blindly inserted into the application.
The AI layer includes:

* Structured response parsing
* JSON validation
* Retry handling for malformed responses
* Response structure validation
* Safety checks
* Separation between AI communication and application logic

This is particularly important for generated quizzes and flashcards, where malformed model output could otherwise result in invalid study material.

---

## Design Principles
SBRAIN was developed around several software-engineering principles:
* **Modularity** — functionality is separated into focused application layers.
* **Separation of concerns** — UI, storage, document processing, knowledge management, and AI logic are kept independent.
* **Local-first design** — personal data can remain entirely on the user's machine.
* **Provider independence** — AI functionality is not tied to a single provider.
* **Persistent storage** — application data survives between sessions through SQLite.
* **Incremental development** — functionality was built progressively from a simple note manager into a larger knowledge and study system.
* **Practical engineering** — the project was developed as a real application rather than as isolated programming exercises.

---

## Project Status
**Current status: B4.0 — Complete**
SBRAIN has reached the intended feature set for this version, including:

* Knowledge management
* SQLite persistence
* Tags and favorites
* Statistics
* Interactive terminal UI
* Responsive note presentation
* Command autocomplete
* Hierarchical help
* Document import
* PDF processing
* PowerPoint processing
* OCR
* Document chunking
* AI integration
* AI-generated summaries
* Flashcards
* Quizzes
* Multiple AI providers
* Local Ollama support
* Configuration management

The project is now considered **feature-complete for its current scope**.
Future changes are expected to be limited primarily to **bug fixes, maintenance, and small corrections discovered through real-world use or external feedback**.

---

## Development Purpose
SBRAIN was created as a personal software-engineering and portfolio project.
The goal was not only to build a useful knowledge-management application, but also to use the project as a practical environment for developing skills in:

* Python
* Object-oriented programming
* Modular architecture
* SQL and SQLite
* Persistent data management
* Terminal UI development
* API integration
* AI integration
* Document processing
* OCR
* Input handling
* Data validation
* Git and version control
* Software-engineering practices

The project evolved from a simple command-line note manager into a modular terminal-based knowledge and study assistant.

---

## License
This project is currently developed as a personal open-source project.
See the repository for the current licensing information.

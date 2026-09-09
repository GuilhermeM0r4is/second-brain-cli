from pathlib import Path

from application.documents.model import Document

from application.material.config import CONSOLE


def import_text(path: Path, dpi: int, language: str) -> Document | None:
    ''' imports content from a txt '''

    try:    # opens the file and uses it to get the components to create the note
        with open(path, "r", encoding = 'utf-8', errors = 'replace') as file:
            text = "\n".join(line.rstrip() for line in file).strip()

        title = path.stem.replace("_", " ").replace("-", " ")
        return Document(title, text, 0, bool(text), False, False)
    
    except FileNotFoundError: CONSOLE.print(f"[red]import_document: File not found[/red]")
    except Exception as e: CONSOLE.print(f"[red]import_documentr: Failed reading text file[/red]")
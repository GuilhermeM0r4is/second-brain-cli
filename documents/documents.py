from pathlib import Path
from material.config import FAVORITE_FALSE, FAVORITE_TRUE, CONSOLE
from material.material import create_note
from documents.text import import_text
from documents.pdf import import_pdf
from documents.pptx import import_pptx
from documents.ocr import is_available, check_ocr_languages
from storage.storage import update_settings, load_settings


IMPORTERS = {
    ".pdf": import_pdf,
    ".pptx": import_pptx,
    ".md": import_text,
    ".txt": import_text
}

def get_info(action: list, siz_action: int) -> tuple[str, str]:
    ''' finds the favorite and tags from a note '''

    tags = ""; fvr = FAVORITE_FALSE

    if siz_action >= 2: tags = action[1]    # checks the len of action to see if we have tags and fvr set up
    
    if siz_action == 3:
        if action[2] in (FAVORITE_FALSE, FAVORITE_TRUE): fvr = action[2]
        else: fvr = FAVORITE_FALSE      # makes it so only 0 or 1 can be used to favorite

    return tags, fvr


def config_dpi(value: int) -> None:
    ''' configures the dpi value to tesseract '''

    if not 76 <= value <= 600: 
        return CONSOLE.print(f"[red]import_config: Invalid dpi value, keep between 76-600.[/red]")

    update_settings(dpi = value)

    return CONSOLE.print(f"[green]import_config: Storage updated, dpi -> {value}[/green]")


def config_lang(language: str) -> None:
    ''' configures the language values to tesseract '''

    if not is_available():
        return CONSOLE.print(f"[red]import_config: Tesserac not installed[/red]")

    if not check_ocr_languages(language):
        return CONSOLE.print(f"[red]import_config: Language(s) not installed in tesseract[/red]")

    update_settings(usr_language = language)

    return CONSOLE.print(f"[green]import_config: Storage updated new {language}[/green]")


def import_documents(actn: list, siz_action: int, dpi: int, language: str) -> None:
    ''' imports all type of documents into functions '''

    if siz_action > 3 or not actn:
        return CONSOLE.print(f"[red]import_documents: Invalid usage[/red]")

    path = Path(actn[0])

    if not path.is_file():
        return CONSOLE.print(f"[red]import_documents: File not found: {path}[/red]")

    extension = path.suffix.lower()

    if extension not in IMPORTERS:
        return CONSOLE.print(f"[red]import_documents: Unsupported file type: {extension}[/red]")


    document = IMPORTERS[extension](path, dpi, language)
    if document is None: return CONSOLE.print(f"[red]import_documents: Document Invalid[/red]")

    tags, fvr = get_info(actn, siz_action)
    print()
    create_note([document.title, document.text, tags, fvr], 4)
    return CONSOLE.print(f"\n[green]import_documents: Note imported successfully[/green]")


def importing(actn: list, siz_action: int) -> None:
    ''' checks the import function, configuration of OCR and importing '''

    if not actn:
        return CONSOLE.print(f"[red]import_documents: Invalid usage[/red]")

    data = load_settings()
    dpi = data["dpi"]; language = data["usr_language"]

    if actn[0] == "-config":
        if siz_action != 1: return CONSOLE.print(f"[red]import_config: Usage: i -config[/red]")

        return CONSOLE.print(f"[green]import_config: {data}[/green]")

    elif actn[0] == "-dpi":
        if siz_action != 2: 
            return CONSOLE.print(f"[red]import_config: Usage: i -dpi | <dpi>[/red]")

        try: dpi = int(actn[1])
        except ValueError: 
            return CONSOLE.print(f"[red]import_config: DPI must be a number[/red]")
        return config_dpi(dpi)

    elif actn[0] == "-lang":
        if siz_action != 2: 
            return CONSOLE.print(f"[red]import_config: Usage: i -lang | <language>[/red]")
        return config_lang(actn[1])

    import_documents(actn, siz_action, dpi, language)
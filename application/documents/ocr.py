import pytesseract
import re
from PIL import Image
from pathlib import Path
from rich.panel import Panel

from application.material.config import CONSOLE


def is_available() -> bool:
    """ returns True if Tesseract OCR is installed and accessible """
    try:
        pytesseract.get_tesseract_version()
        return True

    except pytesseract.TesserdecisionotFoundError: return False


def ask_ocr_print(path: str, pages) -> None:
    ''' prints the console info to ask_ocr function '''

    return CONSOLE.print(
                Panel(
                    f"File: {path.name}\n"
                    f"Pages: {pages}\n\n"
                    "Text found:       ✗\n"
                    "Images found:     ✓\n"
                    "OCR available:    ✓\n\n"
                    "This document appears to contain scanned or "
                    "image-based content.\n\n"
                    "SBRAIN can use Tesseract OCR to extract its text.",
                    title = "DOCUMENT",
                    border_style = "blue"))


def print_ocr_error(path: str, pages) -> None:
    ''' prints the error message when ocr missing '''

    return CONSOLE.print(
                Panel(
                    f"File: {path.name}\n"
                    f"Pages: {pages}\n\n"
                    "Text found:       ✗\n"
                    "Images found:     ✓\n"
                    "OCR available:    ✗\n\n"
                    "This document appears to contain "
                    "image-based content.\n\n"
                    "Tesseract OCR is not installed, so "
                    "SBRAIN cannot extract its text.",
                    title = "DOCUMENT",
                    border_style = "red"))


def ask_ocr(path: Path, pages: int) -> bool:
    """ asks the user whether OCR should be used """
    print()
    
    if is_available():
        ask_ocr_print(path, pages)
        answer = CONSOLE.input("\n[blue]import_documents: Continue with OCR? [y/n]: [/blue]")
        return answer.lower().strip() == "y"

    else:   # not available to usage
        print_ocr_error(path, pages)
        return False


def extract_text(image: Image.Image, language: str) -> str:
    """ extracts text from an image using Tesseract """

    return pytesseract.image_to_string(image, language).strip()


def looks_garbled(text: str, threshold: float = 0.03) -> bool:
    """ hflags text with an unusually high ratio of stray diacritics/ligature artifacts """

    if not text: return False
    artifact_chars = len(re.findall(r'[´¸˜ˆ`]', text))
    return (artifact_chars / max(len(text), 1)) > threshold


def clean_ocr_text(text: str, min_alpha_ratio: float = 0.4) -> str:
    """ removes low-value OCR lines: near-empty lines and lines that are mostly noise """

    if not text: return ""

    cleaned_lines = []
    for line in text.splitlines():

        stripped = line.strip()
        if not stripped: continue

        words = stripped.split()

        alpha_count = sum(c.isalpha() for c in stripped)
        alpha_ratio = alpha_count / len(stripped)

        # drop lines that are mostly symbols/noise (short AND low alpha content)
        if len(stripped) <= 2: continue
        if alpha_ratio < min_alpha_ratio and len(stripped) < 15: continue

        # checks targeting letter-only OCR noise
        if len(words) == 1 and stripped.isupper() and not any(c in "AEIOUaeiou" for c in stripped): continue

        # drop lines that are just the same short token repeated (e.g. "Ny Ny")
        if len(words) >= 2 and len(set(words)) == 1 and len(words[0]) <= 4: continue

        # drop single-token lines shorter than 4 chars unless they look like real short words
        if len(words) == 1 and len(stripped) < 4 and not stripped.isupper(): continue

        cleaned_lines.append(stripped)

    return "\n".join(cleaned_lines)


def check_ocr_languages(language: str) -> bool:
    ''' checks if the requested languages are installed in Tesseract '''
    
    installed = pytesseract.get_languages(config="")
    requested = language.split("+")
    return all(lang in installed for lang in requested)
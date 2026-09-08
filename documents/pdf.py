from pathlib import Path
import pymupdf
import unicodedata
from PIL import Image
from documents.model import Document
from documents.ocr import extract_text, ask_ocr, looks_garbled, clean_ocr_text
from material.config import CONSOLE


def render_page(page, dpi: int) -> Image.Image:
    """ renders a PDF page as a PIL image """

    pixmap = page.get_pixmap(dpi = dpi)
    return Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)


def get_meaningful_images(page, min_area: float = 0.05):
    """ returns images large enough to potentially contain useful information """

    page_area = page.rect.width * page.rect.height
    meaningful = []

    if page_area <= 0: return meaningful

    for image in page.get_image_info():
        bbox = image["bbox"]

        area_ratio = ((bbox[2]-bbox[0]) * (bbox[3]-bbox[1])) / page_area
        if area_ratio >= min_area: meaningful.append(image)

    return meaningful


def import_pdf(path: Path, dpi: int, language: str) -> Document | None:
    """ imports a PDF and optionally uses OCR for image-only or unreliable-text pages """

    text = []; pages = 0
    has_text = False; has_images = False; ocr_used = False

    try:
        with pymupdf.open(path) as pdf:
            pages = len(pdf); page_information = []

            for page in pdf:
                page_text = unicodedata.normalize("NFC", page.get_text("text", sort=True)).strip()
                is_usable = bool(page_text) and not looks_garbled(page_text)

                images = get_meaningful_images(page)

                page_information.append((page, page_text, is_usable, images))

                if is_usable: has_text = True
                if images: has_images = True

            has_ocr_candidates = any((not is_usable) or images for _, _, is_usable, images in page_information)

            use_ocr = False
            if has_ocr_candidates: use_ocr = ask_ocr(path, pages)
            print()

            for page, page_text, is_usable, images in page_information:
                if is_usable and not use_ocr:
                    text.append(page_text)
                    continue

                if use_ocr:
                    image = render_page(page, dpi)
                    ocr_text = clean_ocr_text(extract_text(image, language))

                    if ocr_text:
                        text.append(ocr_text)
                        ocr_used = True

                    elif is_usable: text.append(page_text)

    except Exception as e: return CONSOLE.print(f"[red]import_documents: Error: {e}[/red]")

    title = (path.stem.replace("_", " ").replace("-", " "))
    full_text = "\n\n".join(t for t in text if t.strip())   # skip pages that ended up empty after cleaning

    return Document(title, full_text, pages, has_text, has_images, ocr_used)
from dataclasses import dataclass

@dataclass
class Document:
    title: str
    text: str
    pages: int
    has_text: bool
    has_images: bool
    ocr_used: bool = False
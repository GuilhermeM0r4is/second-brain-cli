from rich.panel import Panel
from application.material.model import Note
from application.material.config import CONSOLE


def note_format_print(note: Note) -> None:
    ''' prints the note in the determined format '''

    print()
    CONSOLE.print(Panel(
        f"[cyan]Id:[/cyan] {note.id}\n\n"
        f"{note.content}\n\n"
        f"[cyan]Tags:[/cyan] {note.tags}\n"
        f"[cyan]Favorite:[/cyan] {note.favorite}\n\n"
        f"[cyan]Created At:[/cyan] {note.created_at[:10]}",
        border_style="cyan", title = note.title), width = 90)
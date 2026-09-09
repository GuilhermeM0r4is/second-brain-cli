from collections.abc import Iterable

from rich.panel import Panel
from rich.table import Table

from application.material.config import CONSOLE
from application.material.model import Note


def note_box(note: Note) -> Panel:
    """ create a panel for a note with a truncated content and tags """

    content = note.content.replace("\n", " ").strip()
    if len(content) > 250: content = content[:250] + "..."
    created_date = note.created_at[:10] if note.created_at else "Unknown"

    return Panel(
        f"[cyan]\nID: {note.id}[/cyan]\n\n{content}\n[dim]"
        f"\nTags: {note.tags}\nCreated: {created_date}[/dim]",
        title = note.title[:32] + "..." if len(note.title) > 32 else note.title,
        border_style = "cyan", expand = True)


def show_notes(notes: Iterable[Note]) -> None:
    """ display notes in a number of columns suited to the terminal width """

    notes_per_row = max(1, min(4, CONSOLE.width // 30))

    table = Table.grid(expand = True, padding = (0, 1))
    table.add_column(ratio = 1)

    for _ in range(notes_per_row - 1):
        table.add_column(ratio = 1)

    row = []
    for note in notes:
        row.append(note_box(note))
        
        if len(row) == notes_per_row:
            table.add_row(*row)
            row = []

    if row:
        row.extend([""] * (notes_per_row - len(row)))
        table.add_row(*row)

    print()
    CONSOLE.print(table)
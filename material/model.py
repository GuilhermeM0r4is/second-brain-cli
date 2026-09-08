from datetime import datetime   # imports the datetime module to work with date and time
from material.config import CONSOLE
from material.config import FAVORITE_FALSE, FAVORITE_TRUE
from dataclasses import dataclass
from rich.panel import Panel

@dataclass      # Uses the note dataclass to
class Note:     # make it more readable
    id: str | None
    title: str
    content: str
    tags: str
    favorite: str
    created_at: str | None = None  # represents as 2026-05-09T15:30:00
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()    


def note_tag_fvr(action: list, siz_action: int) -> tuple[str, str] | None:
    ''' takes the action and turns it into the tags and fvr info '''

    tags = ""; fvr = FAVORITE_FALSE

    # checks the len of action to see if we have tags and fvr set up
    if siz_action >= 3: 
        tags = action[2]
    
    if siz_action == 4:
        if action[3] in (FAVORITE_FALSE, FAVORITE_TRUE):
            fvr = action[3]

        else: fvr = FAVORITE_FALSE   # makes it so only 0 or 1 can be used to favorite

    return tags, fvr


def note_format_print(note: Note) -> None:
    ''' prints the note in the determined format '''

    print()
    CONSOLE.print(Panel(
        f"[cyan]Id:[/cyan] {note.id}\n"
        f"[cyan]Content:[/cyan] {note.content}\n"
        f"[cyan]Tags:[/cyan] {note.tags}\n"
        f"[cyan]Created At:[/cyan] {note.created_at}\n"
        f"[cyan]Favorite:[/cyan] {note.favorite}", 
        border_style="cyan", title = note.title))
from datetime import datetime   # imports the datetime module to work with date and time
from dataclasses import dataclass

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
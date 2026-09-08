from material.config import HELP_COMMAND, FAVORITE_TRUE
from material.model import Note, note_tag_fvr, note_format_print
from material.ui import print_header, CONSOLE
from ai.model import format_quiz_print, format_card_print, FlashCard, Quiz
from storage.storage import (add_note, find_notes_by_tag, load_notes, load_flashcards, load_quizzes, find_note,
                            find_flashcard, load_quiz, delete_note, delete_flashcard, delete_quiz,
                            update_note, update_flashcard, update_quiz, get_connection)


# ---------------------- MAIN FUNCTIONS FOR COMMANDS ----------------------
def create_note(actn: list, siz_action: int) -> None:
    ''' create a note command to add notes database '''

    if siz_action < 2: return CONSOLE.print("[red]create_note: Missing required arguments[/red]")

    # gets the info from the input
    title = actn[0]; content = actn[1]
    tags, fvr = note_tag_fvr(actn, siz_action)
    
    note = Note(id = None, title = title, content = content, tags = tags, favorite = fvr)

    # adds and saves the note into the database
    add_note(note)
    note_format_print(find_note(title))     # prints the note stylized


def list_info(info: str) -> None:
    """ list notes or AI-generated materials by type."""

    if info == "notes":
        notes = load_notes()      # loads all the notes
        if len(notes) == 0: return CONSOLE.print("[red]list_info: No notes[/red]")

        for note in notes: note_format_print(note)  # keep note formatter

    elif info == "cards": 
        cards = load_flashcards()
        if len(cards) == 0: return CONSOLE.print("[red]list_info: No flashcards[/red]")

        for card in cards: format_card_print(card)

    elif info == "quiz":
        quizzes = load_quizzes()
        if len(quizzes) == 0: return CONSOLE.print("[red]list_info: No quizzes[/red]")

        for quiz in quizzes: format_quiz_print(quiz)


def find_info(info: str) -> None:
    ''' searches for a note, or AI-generated content '''

    if len(info) < 2: return CONSOLE.print("[red]find_info: Missing material type or title[/red]")
    kind = info[0]; query = info[1]

    if kind == "notes":    # searches for a note that matches the requirements
        if query[0] == "-":

            tag_name = query[1:]
            results = find_notes_by_tag(tag_name)
            if not results: return CONSOLE.print(f"[red]find_info: No notes found with tag '{tag_name}'[/red]")

            for note in results: note_format_print(note)
            return

        result = find_note(query)
        if isinstance(result, Note): return note_format_print(result)

        return CONSOLE.print("[red]find_info: Note ID or title not found[/red]")

    elif kind == "cards": 
        result = find_flashcard(query)
        if isinstance(result, FlashCard): return format_card_print(result)
        
        return CONSOLE.print("[red]find_info: Flashcard ID or title not found[/red]")

    elif kind == "quiz": 
        result = load_quiz(query)
        
        if isinstance(result, Quiz):    # assures the print of all the tags
            for quiz in result.questions: format_quiz_print(quiz)
            return
        
        return CONSOLE.print("[red]find_info: Quiz ID or title not found[/red]")


def delete_info(info: str) -> None:
    ''' deletes a note in the json file by its id value '''

    if len(info) < 2: return CONSOLE.print("[red]find_info: Missing material type or title[/red]")
    kind = info[0]; query = info[1]

    if kind == "notes":      # working with deleting a note
        if delete_note(query):
            return CONSOLE.print("[green]delete_info: Note deleted[/green]")
                    
        return CONSOLE.print("[red]delete_info: Note ID or title not found[/red]")

    elif kind == "cards":      # working with deleting a note
        if delete_flashcard(query):
            return CONSOLE.print("[green]delete_info: Flashcard deleted[/green]")
                        
        return CONSOLE.print("[red]delete_info: Flashcard ID or title not found[/red]")

    elif kind == "quiz":      # working with deleting a note
            if delete_quiz(query):
                return CONSOLE.print("[green]delete_info: Quiz deleted[/green]")

            return CONSOLE.print("[red]delete_info: Quiz ID or title not found[/red]")


def update_info(actn: list, siz_action: int) -> None:
    ''' updates an already existing material with given information '''

    if siz_action < 3: return CONSOLE.print("[red]update_info: Missing required arguments[/red]")
    kind = actn[0]; query = actn[1]

    if kind == "notes":
        if not (4 <= siz_action <= 6): return CONSOLE.print("[red]update_info: Missing required arguments[/red]")

        note_information = note_tag_fvr(actn[1:], siz_action - 2)

        if note_information is None: return CONSOLE.print("[red]create_note: Use 0 or 1 for favorite option[/red]")
        tags, fvr = note_information

        update_note(query, actn[2], actn[3], tags, fvr)
        return CONSOLE.print("[green]update_info: Note updated successfuly[/green]")

    elif kind == "cards":
        if not siz_action == 5: return CONSOLE.print("[red]update_info: Missing required arguments[/red]")
        update_flashcard(query, actn[2], actn[3], actn[4])
        return CONSOLE.print("[green]update_info: Flashcard updated successfuly[/green]")

    elif kind == "quiz":
        if not siz_action == 3: return CONSOLE.print("[red]update_info: Missing required arguments[/red]")
        update_quiz(query, actn[2])
        return CONSOLE.print("[green]update_info: Quiz updated successfuly[/green]")


def notes_stats() -> None:
    """ prints statistics about notes database """

    with get_connection() as conn:
        total_notes = conn.execute("SELECT COUNT(*) FROM notes").fetchone()[0]

        total_favorites = conn.execute(
            "SELECT COUNT(*) FROM notes WHERE favorite = ?", (FAVORITE_TRUE)).fetchone()[0]

        most_used_tag = conn.execute("""
            SELECT t.name, COUNT(*) AS usage
            FROM tags t
            JOIN note_tags nt ON nt.tag_id = t.id
            GROUP BY t.id, t.name
            ORDER BY usage DESC
            LIMIT 1""").fetchone()

    CONSOLE.print(f"[green]> Total Notes: {total_notes}[/green]")
    CONSOLE.print(f"[green]> Total Favorites: {total_favorites}[/green]")

    if most_used_tag is None: CONSOLE.print("[green]> Most Used Tag: None[/green]")
    else: CONSOLE.print(f"[green]> Most Used Tag: {most_used_tag['name']}[/green]")


def help(actn: list) -> None:
    ''' gives all the information on help command '''

    if actn[0] == "": print_header(); return

    # create a dictionary with all the outcomes to just look through afterwards    
    if actn[0] in HELP_COMMAND: CONSOLE.print(HELP_COMMAND[actn[0]])
    else: CONSOLE.print("[red]help: Invalid choice[/red]")
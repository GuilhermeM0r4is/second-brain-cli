from application.material.config import CONSOLE, FAVORITE_TRUE
from application.material.model import Note
from application.material.formatting import note_format_print

from ui.header import print_header
from ui.listing import show_notes
from ui.helper import HELP_COMMANDS

from application.study.model import FlashCard, Quiz
from application.study.formatting import format_card_print, format_quiz_print

from application.storage.storage import (add_note, find_notes_by_tag, load_notes, load_flashcards, load_quizzes, find_note,
                                        find_flashcard, load_quiz, delete_note, delete_flashcard, delete_quiz,
                                        update_note, update_flashcard, update_quiz, get_connection)

from rich.prompt import Prompt


def input_information(kind: str) -> dict:
    ''' gathers note info interactively, for either create or update '''

    CONSOLE.print(f"[green]{'Creating a new note' if kind == 'create' else 'Updating an existing note'}:[/green]")

    title = CONSOLE.input("[cyan]Title: [/cyan]").strip()
    content = CONSOLE.input("\n[cyan]Content: [/cyan]").strip()
    
    tags_raw = CONSOLE.input("\n[cyan]Tags (comma separated): [/cyan]").strip()
    tags = ",".join(t.strip() for t in tags_raw.split(",") if t.strip())

    favorite = Prompt.ask("\n[cyan]Favorite[/cyan]", choices=["0", "1"], default="0")

    return {"title": title, "content": content, "tags": tags, "favorite": favorite}


def create_note(decision: dict) -> None:
    ''' create a note command to add notes database '''

    if not decision.get("title") or not decision.get("content"):
        return CONSOLE.print("[red]create_note: Missing required arguments[/red]")

    note = Note(id=None, title=decision["title"], content=decision["content"],
                tags=decision["tags"], favorite=decision["favorite"])

    # adds and saves the note into the database
    add_note(note)
    note_format_print(find_note(decision["title"])) # prints the note stylized


def list_info(info: str) -> None:
    """ list notes or AI-generated materials by type."""

    if info == "notes":
        notes = load_notes()      # loads all the notes
        if len(notes) == 0: return CONSOLE.print("[red]list_info: No notes[/red]")

        show_notes(notes)

    elif info == "cards": 
        cards = load_flashcards()
        if len(cards) == 0: return CONSOLE.print("[red]list_info: No flashcards[/red]")

        for card in cards: format_card_print(card)

    elif info == "quiz":
        quizzes = load_quizzes()
        if len(quizzes) == 0: return CONSOLE.print("[red]list_info: No quizzes[/red]")

        for quiz in quizzes:
            full_quiz = load_quiz(str(quiz.id))
            if full_quiz is None: continue

            for question in full_quiz.questions:
                format_quiz_print(Quiz(id=full_quiz.id, title=full_quiz.title,
                                        favorite=full_quiz.favorite, created_at=full_quiz.created_at,
                                        questions=[question]))


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
        
        if isinstance(result, Quiz):
            for q in result.questions:
                format_quiz_print(Quiz(id=result.id, title=result.title, favorite=result.favorite,
                                        created_at=result.created_at, questions=[q]))

        return CONSOLE.print("[red]find_info: Quiz ID or title not found[/red]")


def delete_info(info: str) -> None:
    ''' deletes a note by its id value '''

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

    return CONSOLE.print("[red]delete_info: Type must be 'cards' or 'quiz'[/red]")


def update_info(kind: str, identifier: str, **fields) -> None:
    ''' updates an already existing material with given information '''

    if kind == "notes":
        required = {"title", "content", "tags", "favorite"}
        if not required.issubset(fields):
            return CONSOLE.print("[red]update_info: Missing note information[/red]")

        update_note(identifier, fields["title"], fields["content"],
                    fields["tags"], fields["favorite"])
        
        return CONSOLE.print("[green]update_info: Note updated successfully[/green]")

    elif kind == "cards":
        required = {"title", "front", "back"}
        if not required.issubset(fields):
            return CONSOLE.print("[red]update_info: Missing required arguments[/red]")

        update_flashcard(identifier, fields["title"], fields["front"], fields["back"])
        return CONSOLE.print("[green]update_info: Flashcard updated successfully[/green]")

    elif kind == "quiz":
        if "title" not in fields:
            return CONSOLE.print("[red]update_info: Missing required arguments[/red]")

        update_quiz(identifier, fields["title"])
        return CONSOLE.print("[green]update_info: Quiz updated successfully[/green]")

    else: return CONSOLE.print(f"[red]update_info: Unknown type '{kind}'[/red]")


def notes_stats() -> None:
    """ prints statistics about notes database """

    with get_connection() as conn:
        total_notes = conn.execute("SELECT COUNT(*) FROM notes").fetchone()[0]

        total_favorites = conn.execute(
            "SELECT COUNT(*) FROM notes WHERE favorite = ?", (FAVORITE_TRUE,)).fetchone()[0]

        most_used_tag = conn.execute("""SELECT t.name, COUNT(*) AS usage
                                        FROM tags t
                                        JOIN note_tags nt ON nt.tag_id = t.id
                                        GROUP BY t.id, t.name
                                        ORDER BY usage DESC
                                        LIMIT 1""").fetchone()

    CONSOLE.print(f"[green]> Total Notes: {total_notes}[/green]")
    CONSOLE.print(f"[green]> Total Favorites: {total_favorites}[/green]")

    if most_used_tag is None: CONSOLE.print("[green]> Most Used Tag: None[/green]")
    else: CONSOLE.print(f"[green]> Most Used Tag: {most_used_tag['name']}[/green]")


def help(decision: list) -> None:
    ''' gives all the information on help command '''

    if decision == []: print_header(); return

    # joins the decision list into a string
    decision = " ".join(decision).strip().lower() 
    # create a dictionary with all the outcomes to just look through afterwards    
    if decision in HELP_COMMANDS: CONSOLE.print(HELP_COMMANDS[decision])
    else: CONSOLE.print("[red]help: Invalid choice[/red]")
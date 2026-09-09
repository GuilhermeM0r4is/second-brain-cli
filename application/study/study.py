from application.study.config import sum_note, flashcards, quiz, all_at_once
from application.study.model import Model

from application.material.config import CONSOLE

from application.material.material import find_info, delete_info, list_info, update_info
from application.storage.storage import load_settings


def study(decision: list, size: int) -> None:
    ''' function that uses and executes all study related commands '''

    if size < 1: return CONSOLE.print("[red]study: Missing required arguments[/red]")

    data = load_settings()
    model = Model(data["ai_provider"], data["ai_model"], data["api_key"], data["data_sharing"])

    # joins the decision list into a string
    decision = " ".join(decision).strip().lower() 
    information = decision.split(" ")[1:]

    # available options for the study command
    study_options = {"list": lambda: list_info(information[0] if information else ""),
                     "find": lambda: find_info(information),
                     "delete": lambda: delete_info(information),
                     "update": lambda: study_update(information),
                     "sum": lambda: sum_note(information, model),
                     "cards": lambda: flashcards(information, model),
                     "quiz": lambda: quiz(information, model),
                     "all": lambda: all_at_once(information, model)}

    # chooses the option from the dict
    if decision.split(" ")[0] in study_options: return study_options[decision.split(" ")[0]]() 
    return CONSOLE.print(f"[red]study: wrong command usage[/red]")


def study_update(information: list) -> None:
    ''' auxiliar - updates a flashcard or quiz based on the provided information '''

    if len(information) < 2:
        return CONSOLE.print("[red]study: usage: update cards|quiz <id/title> ...[/red]")

    kind, identifier = information[0], information[1]

    if kind == "cards" and len(information) >= 5:
        return update_info("cards", identifier, title=information[2],
                           front=information[3], back=information[4])

    if kind == "quiz" and len(information) >= 3:
        return update_info("quiz", identifier, title=information[2])

    return CONSOLE.print("[red]study: Missing required arguments[/red]")
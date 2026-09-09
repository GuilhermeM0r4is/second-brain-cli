from application.material.config import CONSOLE
from application.material.material import delete_info, find_info, input_information, list_info, update_info, create_note


def note_decision(decision: list, size: int) -> None:
    ''' handles the decision for the note command '''

    if size == 0: return list_info("notes")

    option = decision[0].strip().lower()

    if option == "create": return create_note(input_information("create"))

    elif option == "list": return list_info("notes")

    elif option == "find":
        if size < 2: return CONSOLE.print("[red]note: Missing search term[/red]")
        return find_info(["notes", decision[1]])

    elif option == "delete":
        if size < 2: return CONSOLE.print("[red]note: Missing note identifier[/red]")
        return delete_info(["notes", decision[1]])

    elif option == "update":
        if size < 2: return CONSOLE.print("[red]note: Missing note identifier[/red]")
        identifier = decision[1]
        fields = input_information("update")
        return update_info("notes", identifier, **fields)

    else: return CONSOLE.print(f"[red]note: Unknown option '{option}'[/red]")
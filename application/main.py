from application.material.config import SEPARATOR, CONSOLE
from application.material.material import notes_stats, help

from application.material.note import note_decision
from application.study.study import study

from application.documents.documents import importing

from application.storage.db import init_db
from application.storage.configure import configure

from ui.input import get_input, print_settings


def main():
    ''' main function that keeps the program running all the time '''

    init_db()   # creates the tables on startup

    while True:
        ''' infinite cycle that allows the user to do all the different tasks '''

        # formats the choice input for the user to use it
        print("\n")
        print_settings()

        inpt = get_input().split(SEPARATOR)
        if not inpt: continue
        print()
      
        # gets the cmd option and the action itself to work with
        command = inpt[0].strip().lower()
        if len(command) > 1: decision = [part.strip() for part in inpt[1:]]
        else: decision = ""

        decision_optn = {"/note": lambda: note_decision(decision, len(decision)),
                        "/stats": lambda: notes_stats(),
                        "/import": lambda: importing(decision, len(decision)),
                        "/study": lambda: study(decision, len(decision)),
                        "/config": lambda: configure(decision, len(decision)),
                        "/help": lambda: help(decision)}

        if command in decision_optn: 
            try: decision_optn[command]()     # chooses the option from the dict
            except Exception as e: CONSOLE.print(f"[red]SBRAIN: {e}[/red]")
      
        elif command == "0": break
        else: CONSOLE.print("[blue]SBRAIN: [red]Invalid choice, use '/help' for help[/red]")
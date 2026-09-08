from storage.storage import load_settings
from ai.config import change_config, reset_config, sum_note, flashcards, quiz, all_at_once
from ai.model import Model, CONSOLE


def ai_tools(actn: list, siz_action: int) -> None:
    ''' function that uses and executes all ai related commands '''

    data = load_settings()
    model = Model(data["ai_provider"], data["ai_model"], data["api_key"], data["data_sharing"])
    
    # shows the current model working / config
    if siz_action == 1 and actn[0] == "-c":
        
        return CONSOLE.print(f"[green]ai_tools: provider: {model.provider} | model: {model.model} | " 
                             f"api_key: {model.api_key} | data_sharing: {model.data_sharing}[/green]")

    # available options for the ai_tools command
    ai_options = {"-c": lambda: change_config(siz_action, model, actn),
                 "-r": lambda: reset_config(), 
                 "sum": lambda: sum_note(actn[1:], model),
                 "cards": lambda: flashcards(actn[1:], model),
                 "quiz": lambda: quiz(actn[1:], model),
                 "all": lambda: all_at_once(actn[1:], model)} 

    if actn[0] in ai_options: return ai_options[actn[0]]()     # chooses the option from the dict
    return CONSOLE.print(f"[red]ai_tools: wrong command usage[/red]")
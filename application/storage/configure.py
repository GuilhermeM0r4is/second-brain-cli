from application.documents.documents import config_dpi, config_lang

from application.study.config import change_config
from application.study.model import Model

from application.material.config import CONSOLE

from application.storage.storage import load_settings


def configure(decision: list, size: int) -> None:
    ''' configures the settings for the application '''

    if size == 0: 
        data = load_settings()
        return CONSOLE.print(f"[green]configure: {data}[/green]")

    option = decision[0].strip().lower()

    if option == "dpi":
        if size < 2: return CONSOLE.print("[red]configure: No dpi value provided[/red]")

        try: value = int(decision[1])
        except ValueError: return CONSOLE.print("[red]configure: Invalid dpi value, must be an integer[/red]")

        return config_dpi(value)

    elif option == "language":
        if size < 2: return CONSOLE.print("[red]configure: No language value provided[/red]")

        language = decision[1].strip()
        return config_lang(language)

    elif option == "ai":
        if size < 2: return CONSOLE.print("[red]configure: No AI configuration provided[/red]")

        settings = load_settings()
        model = Model(settings["ai_provider"], settings["ai_model"], settings["api_key"], settings["data_sharing"])

        return change_config(decision, size, model)

    else: return CONSOLE.print(f"[red]configure: Unknown option '{option}'[/red]")
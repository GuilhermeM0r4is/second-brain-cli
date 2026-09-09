from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import VSplit, Window
from prompt_toolkit.widgets import Frame, TextArea
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import FormattedText

from application.material.config import CONSOLE
from application.storage.storage import load_settings

from ui.completer import TreeCompleter

def get_input() -> str:
    """ opens the SBRAIN input box and returns the text entered by the user """

    # editable input box for the user to type in -> stores .text
    input_box = TextArea(multiline = False, wrap_lines = False,
                        scrollbar = False, height = 1, 
                        prompt = FormattedText([("fg:ansigreen", " SBRAIN > ")]),
                        completer = TreeCompleter(), complete_while_typing = True, style = "class:input-field")

    # key bindings for the input box
    kb = KeyBindings()

    @kb.add("enter")    # adds functionality to the enter key
    def _(event): event.app.exit(result=input_box.text)

    layout = Layout(
                VSplit([
                    Frame(input_box, width = 65),
                    Window(),
                    Window()
                ]),
            )
    # apps configuration -> change for different apps settings
    app = Application(layout = layout, key_bindings = kb,
                      full_screen = False, mouse_support = False)

    return app.run()


def print_settings() -> None:
    """ prints the current settings to the console """

    settings = load_settings()
    return CONSOLE.print(
                    f"[blue]   LANG:[/blue] {settings['usr_language']}     "
                    f"[blue]PROVIDER:[/blue] {settings['ai_provider']}     "
                    f"[blue]MODEL:[/blue] {settings['ai_model']}")
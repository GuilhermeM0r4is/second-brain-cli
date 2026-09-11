from ui.header import print_header

HELP_COMMANDS = {"": lambda: print_header(),

                "note": ("\n[green]/note commands[/green]\n\n"
                         "[cyan]> create[/cyan]\n"
                         "[cyan]> list[/cyan]\n"
                         "[cyan]> find[/cyan] (id/title) / tag\n"
                         "[cyan]> delete[/cyan] id/title\n"
                         "[cyan]> update[/cyan] id/title new_title [content] [tags] [fvr]\n"
                         "\n[blue]example_usage: [/blue]/note create"),

                "note create": ("\n[green]/note create: creates a new note[/green]"
                                "\n[green]Creates a new note using a input based logic[/green]"),

                "note list": ("\n[green]/note list: lists stored material[/green]"
                              "\n[green]Displays all notes in a table, depending on the width of the interface[/green]"),

                "note find": ("\n[green]/note find: searches stored material[/green]\n\n"
                              "[cyan]> id/title: [/cyan]find a note by ID or title;\n"
                              "[cyan]>tag <tag>: [/cyan]find notes by tag;\n"
                              "\n[blue]usage: [/blue]/note find 8"
                              "\n[blue]usage: [/blue]/note find tag biology"),

                "note delete": ("\n[green]/note delete: deletes stored material[/green]\n\n"
                                "[cyan]> id/title: [/cyan]delete a note;\n"
                                "\n[blue]usage: [/blue]/note delete really_cool_title"),

                "note update": ("\n[green]/note update: updates stored material[/green]\n\n"
                                "\n[green]Updates an existing note using a input based logic[/green]"),

                "stats": ("\n[green]/stats: shows note statistics[/green]\n"
                          "Displays total notes, favorite notes, and the most-used tag."),

                "config": ("\n[green]/config commands[/green]\n\n"
                           "[cyan]> dpi[/cyan] value\n"
                           "[cyan]> language[/cyan] language or language list\n"
                           "[cyan]> ai[/cyan] provider:provider api_key:api_key model:model\n"
                           "\n[blue]usage: [/blue]/config ai provider:ollama model:qwen3.5:27b"),

                "config dpi": ("\n[green]/config dpi: configures OCR resolution[/green]\n\n"
                               "[cyan]> value: [/cyan]an integer from 76 to 600.\n"
                               "\n[blue]usage: [/blue]/config dpi 300"),

                "config language": ("\n[green]/config language: configures OCR language(s)[/green]\n\n"
                                    "[cyan]> language: [/cyan]installed Tesseract language code(s), such as eng or eng+por.\n"
                                    "\n[blue]usage: [/blue]/config language | eng+por"),

                "config ai": ("\n[green]/config ai: configures the AI model[/green]\n\n"
                              "[cyan]provider: [/cyan]ollama, openai, anthropic, or gemini;\n"
                              "[cyan]api_key: [/cyan]provider API key, when required;\n"
                              "[cyan]model: [/cyan]model name used by the provider.\n"
                              "\n[blue]usage: [/blue]/config ai | provider:openai | api_key:<key> | model:gpt-4o"),

                "import": ("\n[green]/import: imports a document into notes[/green]\n"
                           "[green]Supports PDF, PPTX, and Markdown documents.[/green]\n"
                           "\n[blue]usage: [/blue]/import <document> [tags] [fvr]"),

                "study": ("\n[green]/study commands: helps you manage your study materials[/green]"
                          "\n[green]type includes both: 'cards' and 'quiz'[/green]\n\n"
                          "[cyan]> list[/cyan] type\n"
                          "[cyan]> find[/cyan] type id/title\n"
                          "[cyan]> delete[/cyan] type id/title\n"
                          "[cyan]> update[/cyan] type id/title content\n"
                          "     [cyan]- cards id/title new_title [front] [back]: [/cyan]update a flashcard;\n"
                          "     [cyan]- quiz id/title new_title: [/cyan]update a quiz.\n"
                          "[cyan]> sum[/cyan] id/title\n"
                          "[cyan]> cards[/cyan] id/title\n"
                          "[cyan]> quiz[/cyan] id/title\n"
                          "[cyan]> all[/cyan] id/title\n"
                          "\n[blue]usage: [/blue]/study find cards biology"
                          "\n[blue]usage: [/blue]/study delete cards 9"
                          "\n[blue]usage: [/blue]/study update cards 9 new_title new_front new_back"
                          "\n[blue]usage: [/blue]/study sum 9"),

                      "study delete": ("\n[green]/study delete: deletes generated study material[/green]\n\n"
                                 "[cyan]> type: [/cyan]cards or quiz;\n"
                                 "[cyan]> id/title: [/cyan]the flashcard or quiz to delete.\n"
                                 "\n[blue]usage: [/blue]/study delete cards 9"
                                 "\n[blue]usage: [/blue]/study delete quiz 2")}



COMMAND_TREE = {
    
    "note": {
        "description": "Manage notes",
        "usage": "",
        "help": ("\n[green]/note commands[/green]\n\n"
                 "[cyan]> create[/cyan] title content [tags] [fvr]\n"
                 "[cyan]> list[/cyan]\n"
                 "[cyan]> find[/cyan] (id/title) / tag\n"
                 "[cyan]> delete[/cyan] id/title\n"
                 "[cyan]> update[/cyan] id/title new_title [content] [tags] [fvr]\n"
                 "\n[blue]example_usage: [/blue]/note create"),
        "subcommands": {
            "create": {
                "description": "Create a new note",
                "usage": "title content [tags] [fvr]",
                "help": ("\n[green]/note create: creates a new note[/green]\n\n"
                          "[cyan]> title: [/cyan]title that describes the note;\n"
                          "[cyan]> content: [/cyan]text to store in the note;\n"
                          "[cyan]> tags: [/cyan]optional tags separated according to the command input format;\n"
                          "[cyan]> fvr: [/cyan]favorite flag: 0 for false or 1 for true.\n"
                          "\n[blue]usage: [/blue]/note create title_2 how_to_basic cooking 0"),
                "subcommands": {},
            },
            "list": {
                "description": "List stored notes",
                "usage": "",
                "help": ("\n[green]/note list: lists stored material[/green]\n"
                          "Displays all notes in a table, depending on the width of the interface\n"),
                "subcommands": {},
            },
            "find": {
                "description": "Search notes",
                "usage": "(id/title) / tag",
                "help": ("\n[green]/note find: searches stored material[/green]\n\n"
                          "[cyan]> id/title: [/cyan]find a note by ID or title;\n"
                          "[cyan]>tag <tag>: [/cyan]find notes by tag;\n"
                          "\n[blue]usage: [/blue]/note find 8"
                          "\n[blue]usage: [/blue]/note find tag biology"),
                "subcommands": {},
            },
            "delete": {
                "description": "Delete a note",
                "usage": "id/title",
                "help": ("\n[green]/note delete: deletes stored material[/green]\n\n"
                          "[cyan]> id/title: [/cyan]delete a note;\n"
                          "\n[blue]usage: [/blue]/note delete really_cool_title"),
                "subcommands": {},
            },
            "update": {
                "description": "Update a note",
                "usage": "id/title new_title [content] [tags] [fvr]",
                "help": ("\n[green]/note update: updates stored material[/green]\n\n"
                          "[cyan]> id/title new_title [content] [tags] [fvr]: [/cyan]update a note;\n"
                          "\n[blue]usage: [/blue]/note update 9 new_title cool_content tag2 1"),
                "subcommands": {},
            },
        },
    },

    "stats": {
        "description": "Show note statistics",
        "usage": "",
        "help": ("\n[green]/stats: shows note statistics[/green]\n"
                  "Displays total notes, favorite notes, and the most-used tag."),
        "subcommands": {},
    },

    "help": {
        "description": "Show command help",
        "usage": "",
        "help": "",
        "subcommands": {
            "note": {
                "description": "Show note command help",
                "usage": "",
                "help": "",
                "subcommands": {
                    "create": {"description": "Show note create help", "usage": "", "help": "", "subcommands": {}},
                    "list": {"description": "Show note list help", "usage": "", "help": "", "subcommands": {}},
                    "find": {"description": "Show note find help", "usage": "", "help": "", "subcommands": {}},
                    "delete": {"description": "Show note delete help", "usage": "", "help": "", "subcommands": {}},
                    "update": {"description": "Show note update help", "usage": "", "help": "", "subcommands": {}},
                },
            },
            "stats": {
                "description": "Show statistics help",
                "usage": "",
                "help": "",
                "subcommands": {},
            },
            "config": {
                "description": "Show configuration help",
                "usage": "",
                "help": "",
                "subcommands": {
                    "dpi": {"description": "Show OCR resolution help", "usage": "", "help": "", "subcommands": {}},
                    "language": {"description": "Show OCR language help", "usage": "", "help": "", "subcommands": {}},
                    "ai": {"description": "Show AI configuration help", "usage": "", "help": "", "subcommands": {}},
                },
            },
            "import": {
                "description": "Show document import help",
                "usage": "",
                "help": "",
                "subcommands": {},
            },
            "study": {
                "description": "Show study command help",
                "usage": "",
                "help": "",
                "subcommands": {
                    "delete": {"description": "Show study delete help", "usage": "", "help": "", "subcommands": {}},
                },
            },
        },
    },

    "config": {
        "description": "Configure SBRAIN",
        "usage": "",
        "help": ("\n[green]/config commands[/green]\n\n"
                  "[cyan]> dpi[/cyan] value\n"
                  "[cyan]> language[/cyan] language or language list\n"
                  "[cyan]> ai[/cyan] provider:provider api_key:api_key model:model\n"
                  "\n[blue]usage: [/blue]/config ai provider:ollama model:qwen3.5:27b"),
        "subcommands": {
            "dpi": {
                "description": "Configure OCR resolution",
                "usage": "value",
                "help": ("\n[green]/config dpi: configures OCR resolution[/green]\n\n"
                          "[cyan]> value: [/cyan]an integer from 76 to 600.\n"
                          "\n[blue]usage: [/blue]/config dpi 300"),
                "subcommands": {},
            },
            "language": {
                "description": "Configure OCR languages",
                "usage": "language",
                "help": ("\n[green]/config language: configures OCR language(s)[/green]\n\n"
                          "[cyan]> language: [/cyan]installed Tesseract language code(s), such as eng or eng+por.\n"
                          "\n[blue]usage: [/blue]/config language | eng+por"),
                "subcommands": {},
            },
            "ai": {
                "description": "Configure the AI model",
                "usage": "provider:<provider> | api_key:<key> | model:<model>",
                "help": ("\n[green]/config ai: configures the AI model[/green]\n\n"
                          "[cyan]provider: [/cyan]ollama, openai, anthropic, or gemini;\n"
                          "[cyan]api_key: [/cyan]provider API key, when required;\n"
                          "[cyan]model: [/cyan]model name used by the provider.\n"
                          "\n[blue]usage: [/blue]/config ai | provider:openai | api_key:<key> | model:gpt-4o"),
                "subcommands": {},
            },
        },
    },

    "import": {
        "description": "Import a document into notes",
        "usage": "<document> [tags] [fvr]",
        "help": ("\n[green]/import: imports a document into notes[/green]\n"
                  "[green]Supports PDF, PPTX, and Markdown documents.[/green]\n"
                  "\n[blue]usage: [/blue]/import <document> [tags] [fvr]"),
        "subcommands": {},
    },

    "study": {
        "description": "Manage study material (cards and quiz)",
        "usage": "",
        "help": ("\n[green]/study commands: helps you manage your study materials[/green]"
                  "\n[green]type includes both: 'cards' and 'quiz'[/green]\n\n"
                  "[cyan]> list[/cyan] type\n"
                  "[cyan]> find[/cyan] type id/title\n"
                  "[cyan]> delete[/cyan] type id/title\n"
                  "[cyan]> update[/cyan] type id/title content\n"
                  "     [cyan]- cards id/title new_title [front] [back]: [/cyan]update a flashcard;\n"
                  "     [cyan]- quiz id/title new_title: [/cyan]update a quiz.\n"
                  "[cyan]> sum[/cyan] id/title\n"
                  "[cyan]> cards[/cyan] id/title\n"
                  "[cyan]> quiz[/cyan] id/title\n"
                  "[cyan]> all[/cyan] id/title\n"
                  "\n[blue]usage: [/blue]/study find cards biology"
                  "\n[blue]usage: [/blue]/study delete cards 9"
                  "\n[blue]usage: [/blue]/study update cards 9 new_title new_front new_back"
                  "\n[blue]usage: [/blue]/study sum 9"),
        "subcommands": {
            "list": {
                "description": "List study material",
                "usage": "type",
                "help": "",   # only described inline within /study, no dedicated entry yet
                "subcommands": {},
            },
            "find": {
                "description": "Find study material",
                "usage": "type id/title",
                "help": "",
                "subcommands": {},
            },
            "delete": {
                "description": "Delete generated study material",
                "usage": "type id/title",
                "help": ("\n[green]/study delete: deletes generated study material[/green]\n\n"
                          "[cyan]> type: [/cyan]cards or quiz;\n"
                          "[cyan]> id/title: [/cyan]the flashcard or quiz to delete.\n"
                          "\n[blue]usage: [/blue]/study delete cards 9"
                          "\n[blue]usage: [/blue]/study delete quiz 2"),
                "subcommands": {},
            },
            "update": {
                "description": "Update study material",
                "usage": "type id/title new_title ...",
                "help": "",
                "subcommands": {
                    "cards": {
                        "description": "Update a flashcard",
                        "usage": "id/title new_title [front] [back]",
                        "help": "",
                        "subcommands": {},
                    },
                    "quiz": {
                        "description": "Update a quiz",
                        "usage": "id/title new_title",
                        "help": "",
                        "subcommands": {},
                    },
                },
            },
            "sum": {
                "description": "Generate a note summary",
                "usage": "id/title",
                "help": "",
                "subcommands": {},
            },
            "cards": {
                "description": "Generate flashcards",
                "usage": "id/title",
                "help": "",
                "subcommands": {},
            },
            "quiz": {
                "description": "Generate a quiz",
                "usage": "id/title",
                "help": "",
                "subcommands": {},
            },
            "all": {
                "description": "Generate summary, flashcards, and quiz at once",
                "usage": "id/title",
                "help": "",
                "subcommands": {},
            },
        },
    },
}
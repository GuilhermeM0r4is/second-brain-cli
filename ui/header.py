from application.material.config import CONSOLE

banner = """[bold cyan]

        ███████╗██████╗ ██████╗  █████╗ ██╗███╗   ██╗
        ██╔════╝██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║
        ███████╗██████╔╝██████╔╝███████║██║██╔██╗ ██║
        ╚════██║██╔══██╗██╔══██╗██╔══██║██║██║╚██╗██║
        ███████║██████╔╝██║  ██║██║  ██║██║██║ ╚████║
        ╚══════╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝
[/bold cyan]
                     SBRAIN-CLI • B4.0
"""

# set up the header for later usage
header = """
    [bold blue]SBRAIN COMMANDS[/bold blue]

    [green]>[/green] [blue]/note[/blue]
        [cyan]create[/cyan]
        [cyan]list[/cyan]
        [cyan]find[/cyan]   note_id | title | tag <tag>
        [cyan]delete[/cyan] note_id | title | tag <tag>
        [cyan]update[/cyan] note_id | title

    [green]>[/green] [blue]/stats[/blue]
        Show notes and system statistics

    [green]>[/green] [blue]/import[/blue]
        Import notes from a document

    [green]>[/green] [blue]/study[/blue]
        [cyan]list[/cyan]    type
        [cyan]find[/cyan]    type | query
        [cyan]delete[/cyan]  type | id/title
        [cyan]update[/cyan]  type | note_id | content
        [cyan]sum[/cyan]     note_id | title
        [cyan]cards[/cyan]   note_id | title
        [cyan]quiz[/cyan]    note_id | title
        [cyan]all[/cyan]     note_id | title

    [green]>[/green] [blue]/config[/blue]
        [cyan]dpi[/cyan]         value
        [cyan]language[/cyan]    value
        [cyan]ai[/cyan]          provider:openai model:gpt5.6-luna api_key:key
        
    [green]>[/green] [blue]/help[/blue]
        note | note find | study | study find | ...

    [red]0.[/red] Exit"""

def print_header() -> None:
    ''' prints the header - that's all it does '''
    CONSOLE.print(header)    # prints the header


def print_info() -> None:
    ''' print function for the intro messages '''
    CONSOLE.print(banner)     # prints the banner in center
    print_header()
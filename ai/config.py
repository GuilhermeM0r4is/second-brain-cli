from ai.model import (Model, get_flashcard_prompt, get_quiz_prompt, get_sumchunk_prompt, get_synthesis_prompt,
                      format_card_print, format_quiz_print)
from ai.parsing import parse_chunk_summary, parse_synthesis, parse_flashcards, parse_quiz
from ai.safe_guarding import ensure_model, ask_parsed_with_retry
from material.material import create_note
from material.model import Note, CONSOLE
from storage.storage import find_note, update_settings, add_flashcard, add_quiz
import re

MATH_DENSITY_THRESHOLD = 0.02
MAX_CHARS = 7000


def helper_note_restrictions(actn: str, model: Model) -> Note | None:
    ''' gets the note and checks all restrictions of functions '''

    if not ensure_model(model): return CONSOLE.print("[red]ai_tools: Invalid model[/red]")
    return find_note(actn)


# ------------------------ CONFIG BASED FUNCTIONS ------------------------
def change_config(siz_action: int, model: Model, actn: list) -> None:
    ''' function that changes the configuration of the AI model '''

    if siz_action == 1: return CONSOLE.print(f"[green]ai_config: {model}[/green]")
    if siz_action < 2: return CONSOLE.print(f"[red]ai_config: Invalid action[/red]")

    for num in range(1, siz_action):

        # if the action is not in the correct format, we skip it
        if ":" not in actn[num]: return CONSOLE.print(f"[red]ai_config: Invalid action format: {actn[num]}[/red]")

        key, value = actn[num].split(":", 1)     # splits the action into key and value
        key = key.strip()
        value = value.strip()

        if key not in ["provider", "model", "api_key"]: return CONSOLE.print(f"[red]ai_config: Invalid key: {key}[/red]")

        if key == "api_key" and value != "":
            CONSOLE.print(f"\n[yellow]ai_config: Warning: You are using a non-local model, keep in mind that your data may be shared![/yellow]")
            setattr(model, "data_sharing", "CLOUD")  # sets the data sharing to ON if the api_key is not empty

        # updates the model with the new key-value pair
        setattr(model, key, value)      # sets the attribute of the model to the new value

    CONSOLE.print(f"[green]ai_config: Updated AI info to: provider: {model.provider}" 
                  f"model: {model.model} | data_sharing: {model.data_sharing}[/green]")

    update_settings(ai_provider = model.provider, ai_model = model.model, 
                    api_key = model.api_key, data_sharing = model.data_sharing)
    return


def reset_config() -> None:
    ''' resets the configuration of the AI model to default values '''
    
    update_settings(ai_provider = "ollama", ai_model = "NONE", api_key = "NONE", data_sharing = "LOCAL")
    CONSOLE.print(f"[green]ai_config: provider: ollama | model: NONE | " 
                  f"api_key: NONE | data_sharing: LOCAL[/green]")


# ------------------------ SUMMARIZING BASED FUNCTIONS ------------------------
def split_note(content: str) -> list[str]:
    ''' splits a note into smaller notes '''

    paragraphs = content.split("\n\n")
    chunks = []; current = ""

    for paragraph in paragraphs:
        if len(current) + len(paragraph) > MAX_CHARS:

            if current: chunks.append(current.strip())
            current = paragraph

        else: current += "\n\n" + paragraph

    if current.strip(): chunks.append(current.strip())
    return chunks


MATH_SYMBOL_PATTERN = re.compile(
    r'[∂∇∫∑√±≤≥≠∈⊂⊆∀∃⇒⇔→↦×÷·∞]|\\frac|\\partial|\\nabla|\\int|\\sum|\\lim|\\sqrt|\\mathbf|\\begin\{')

# common leftover patterns from OCR'd math: "R2", "R3", "Rn", digit-glued-to-letter like "y2", "x2"
MATH_STRUCTURAL_PATTERN = re.compile(
    r'\bR\d\b|\bR[nm]\b|\b[a-zA-Z]\d\b|\b\d[a-zA-Z]\b|f\([a-zA-Z],\s*[a-zA-Z]\)|D[a-zA-Z]?f\(|∀|∃')


def math_density(content: str) -> float:
    """ estimates how math-heavy a note is, combining symbol/structural markers and topic keywords """

    if not content: return 0.0
    words = content.split()
    word_count = max(len(words), 1)

    symbol_hits = len(MATH_SYMBOL_PATTERN.findall(content))
    structural_hits = len(MATH_STRUCTURAL_PATTERN.findall(content))

    total_hits = (symbol_hits * 2) + structural_hits
    return total_hits / word_count


def is_math_heavy(content: str) -> bool:
    ''' helper function that decides if a note is math-heavy in content '''
    
    if math_density(content) > MATH_DENSITY_THRESHOLD:

        CONSOLE.print("[yellow]ai_tools: This note is math-heavy — results may be "
                      "less precise for equations. Formulas will be described "
                      "rather than reproduced exactly where needed.[/yellow]")
        return True

    return False

def summarize_chunk(title: str, content: str, model: Model, math_heavy: bool) -> dict | None:
    ''' summarizes a small note chunck and returns the response '''

    prompt = get_sumchunk_prompt(title, content, math_heavy)
    return ask_parsed_with_retry(prompt, model, parse_chunk_summary, max_tokens = 1500) or None


def synthesize_summaries(title: str, summaries: list[dict], model: Model) -> dict | None:
    ''' synthesizes all note chuncks and returns the finel answer '''

    prompt = get_synthesis_prompt(title, summaries)
    return ask_parsed_with_retry(prompt, model, parse_synthesis, max_tokens = 3000) or None


def summarize_large_note(title: str, content: str, model: Model, math_heavy: bool) -> dict | None:
    """ summarizes a large note splitting it into chunks """

    chunks = split_note(content)
    summaries = []

    for number, chunk in enumerate(chunks, start = 1):
        CONSOLE.print(f"[blue]ai_sum: Analyzing section {number}/{len(chunks)}...[/blue]")

        summary = summarize_chunk(title, chunk, model, math_heavy)
        if summary: summaries.append(summary)

    if not summaries: return None
    CONSOLE.print("[blue]ai_sum: Starting to synthesize the summaries[/blue]\n")

    return synthesize_summaries(title, summaries, model)


def sum_note(actn: list, model: Model) -> None:
    ''' summarizes a note using the AI model '''
    try:
        result = helper_note_restrictions(actn[0], model)
        if not result: return CONSOLE.print("[red]ai_sum: Note not found[/red]")

        heavy = is_math_heavy(result.content)
        answer = summarize_large_note(result.title, result.content, model, math_heavy = heavy)

        if not answer:
            return CONSOLE.print("[red]ai_sum: AI returned invalid answer[/red]")

        if "title" not in answer or "summary" not in answer:
            return CONSOLE.print("[red]ai_sum: AI returned invalid answer[/red]")

        # carry over the original note's tags, appending "sum" to mark it as a generated summary
        existing_tags = [t.strip() for t in result.tags.split(",") if t.strip()] if result.tags else []

        if "sum" not in existing_tags: existing_tags.append("sum")
        tags = ",".join(existing_tags)

        create_note([answer["title"], answer["summary"], tags, result.favorite], 4)
        return CONSOLE.print("\n[green]ai_sum: Note summarized and added to database[/green]")

    except ValueError as e: return CONSOLE.print(f"[red]ai_sum: {e}[/red]")


# ------------------------ FLASHCARD + QUIZ BASED FUNCTIONS ------------------------
def flashcards(actn: list, model: Model) -> None:
    ''' creates flashcards from a given note (should use summarized notes) '''

    try:
        result = helper_note_restrictions(actn[0], model)
        if not result: return CONSOLE.print("[red]ai_sum: Note not found[/red]")

        heavy = is_math_heavy(result.content)

        prompt = get_flashcard_prompt(result.title, result.content, heavy)
        cards = ask_parsed_with_retry(prompt, model, parse_flashcards, max_tokens = 2000)

        if not cards:
            return CONSOLE.print("[red]ai_flashcard: AI returned no usable flashcards[/red]")

        for flashcard in cards:
            format_card_print(flashcard["front"], flashcard["back"], flashcard["title"])
            add_flashcard(flashcard)

        return CONSOLE.print(f"\n[green]ai_flashcard: {len(cards)}x Flashcards generated.[/green]")

    except ValueError as e: return CONSOLE.print(f"[red]ai_flashcard: {e}[/red]")


def quiz(actn: list, model: Model) -> None:
    ''' creates flashcards from a given note (should use summarized notes) '''

    try:
        result = helper_note_restrictions(actn[0], model)
        if not result: return CONSOLE.print("[red]ai_sum: Note not found[/red]")
        
        heavy = is_math_heavy(result.content)

        prompt = get_quiz_prompt(result.title, result.content, heavy)
        questions = ask_parsed_with_retry(prompt, model, parse_quiz, max_tokens = 2000)

        if not questions:
            return CONSOLE.print("[red]ai_quiz: AI returned no usable quiz questions[/red]")

        for quest in questions:
            format_quiz_print(quest["question"], quest["options"], quest["correct_answer"],
                               quest["explanation"], quest["title"])
            add_quiz(quest)

        return CONSOLE.print(f"\n[green]ai_quiz: {len(questions)}x Quiz generated.[/green]")

    except ValueError as e: return CONSOLE.print(f"[red]ai_quiz: {e}[/red]")


def all_at_once(actn: list, model: Model) -> None:
    ''' does all the three generations at once '''
    try:
        sum_note(actn, model)
        flashcards(actn, model)
        quiz(actn, model)
    
    except ValueError as e: return CONSOLE.print(f"[red]ai_tools: {e}[/red]")

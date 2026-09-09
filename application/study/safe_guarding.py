from application.study.communication import ask_ai
from application.study.model import Model

from application.material.config import CONSOLE

def ask_with_retry(prompt: str, model: Model, max_tokens: int) -> str | None:
    """ Sends a prompt to the AI model and retries if it fails."""

    retries = 3
    for attempt in range(1, retries + 1):
        try: 
            return ask_ai(prompt, model, max_tokens)
        
        except Exception as e:
            if attempt == retries:
                CONSOLE.print(f"[red]ai_tools: AI request failed after {retries} attempts: {e}[/red]")
                return None

            CONSOLE.print(f"[yellow]ai_tools: Retry {attempt}/{retries}...[/yellow]")

    return None


def ensure_model(model: Model) -> bool:
    ''' ensures that the model is valid and ready to use '''

    if model is None or not isinstance(model, Model) or model.model == "NONE":
        CONSOLE.print("[red]ai_tools: No model configuration found. Please set the provider and model before using AI features.[/red]")
        return False

    if model.provider not in ["ollama", "openai", "anthropic", "gemini"]:
        CONSOLE.print("[red]ai_tools: Invalid model configuration. Please set the provider and model before using AI features.[/red]")
        return False

    if model.provider in ["openai", "anthropic", "gemini"] and (model.api_key is None or model.api_key == "NONE"):
        CONSOLE.print("[red]ai_tools: No API key found for the selected provider. Please set the API key before using AI features.[/red]")
        return False

    return True


def ask_parsed_with_retry(prompt: str, model: Model, parser, max_tokens: int) -> dict | list[dict] | None:
    """ asks the model for plain text output and retries if parsing fails. """

    current_prompt = prompt
    retries = 3

    for attempt in range(1, retries + 1):
        raw = ask_with_retry(current_prompt, model, max_tokens)
        if raw is None: return None

        result = parser(raw)
        if result: return result

        if attempt < retries:
            CONSOLE.print(f"[yellow]ai_tools: Invalid output format, retrying ({attempt}/{retries})...[/yellow]")
            current_prompt = prompt + """ Your previous response did not follow the required format exactly.
                                          Try again. Use the exact labels and markers shown, plain text only. """
    return None
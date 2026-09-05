from ai.model import Model
from material.config import CONSOLE

def ask_ollama(prompt: str, model: Model, max_tokens: int) -> str | None:
    ''' function that sends a prompt to the Ollama model and returns the response '''
    import ollama

    message = [{"role": "user", "content": prompt}]
    options = {"temperature": 0.2,
                "num_ctx": 4096,       # give it real room — your chunks alone eat ~2300 tokens
                "num_predict": max_tokens,   # hard cap output length so a stuck/looping generation can't run forever
                "num_thread": 4}       # try 4, 6, 8 and compare speed/heat tradeoff

    if model.data_sharing == "LOCAL":   # uses local ollama to try to resume the note
        response = ollama.chat(
            model = model.model,
            messages = message,
            options = options
        )
    elif model.data_sharing == "CLOUD":     # uses api_key ollama to try to resume the note
        client = ollama.Client(
            host = "https://ollama.com",
            headers = {"Authorization": f"Bearer {model.api_key}"})
        
        response = client.chat(
            model = model.model,
            messages = message,
            options = options
        )
    else: return CONSOLE.print(f"[red]ai_tools: Invalid data sharing option: {model.data_sharing}[/red]")
    return response.message.content


def ask_openai(prompt: str, model: Model) -> str:
    ''' function that sends a prompt to the OpenAI model and returns the response '''

    from openai import OpenAI
    client = OpenAI(api_key = model.api_key)

    response = client.responses.create(
        model = model.model,
        input = prompt
    )
    return response.output_text


def ask_anthropic(prompt: str, model: Model) -> str:
    ''' function that sends a prompt to the Anthropic model and returns the response '''

    from anthropic import Anthropic
    client = Anthropic(api_key = model.api_key)
    response = client.messages.create(
        model = model.model,
        max_tokens = 4096,
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.content[0].text


def ask_gemini(prompt: str, model: Model) -> str:
    ''' function that sends a prompt to the Gemini model and returns the response '''

    from google import genai
    client = genai.Client(api_key = model.api_key)
    response = client.models.generate_content(
        model = model.model,
        contents = prompt
    )
    return response.text


def ask_ai(prompt: str, model: Model, max_tokens: int) -> str | None:
    ''' function that sends a prompt to the AI model and returns the response '''

    if model is None: return CONSOLE.print("[red]Model config is missing[/red]")

    if model.provider == "ollama":      # gotta have both LOCAL and CLOUD options
        return ask_ollama(prompt, model, max_tokens)

    elif model.provider == "openai":
        if not model.api_key or model.api_key == "NONE": return CONSOLE.print("[red]OpenAI API key is missing[/red]")
        return ask_openai(prompt, model)
    
    elif model.provider == "anthropic":
        if not model.api_key or model.api_key == "NONE": return CONSOLE.print("[red]Anthropic API key is missing[/red]")
        return ask_anthropic(prompt, model)

    elif model.provider == "gemini":
        if not model.api_key or model.api_key == "NONE": return CONSOLE.print("[red]Gemini API key is missing[/red]")
        return ask_gemini(prompt, model)

    return CONSOLE.print(f"[red]ai_tools: Invalid provider: {model.provider}[/red]")
import re

def get_field(block: str, label: str) -> str:
    ''' extracts a single-line field value like "LABEL: value" from a text block '''

    match = re.search(rf'{label}\s*:\s*(.+)', block, re.IGNORECASE)
    return match.group(1).strip() if match else ""


def get_multiline_field(block: str, label: str, stop_labels: list[str]) -> str:
    ''' extracts a field that can span multiple lines, until the next known label '''

    stop_pattern = "|".join(stop_labels) if stop_labels else r'\Z'

    match = re.search(rf'{label}\s*:\s*(.*?)(?=\n\s*(?:{stop_pattern})\s*:|\Z)',
                      block, re.IGNORECASE | re.DOTALL)

    return match.group(1).strip() if match else ""


def parse_chunk_summary(text: str) -> dict:
    ''' parses a SUMMARY / KEY_POINTS text block '''

    if not text: return {}

    summary = get_multiline_field(text, "SUMMARY", ["KEY_POINTS"])
    points_block = get_multiline_field(text, "KEY_POINTS", [])

    key_points = []
    for line in points_block.splitlines():
        line = line.strip().lstrip("-•*").strip()

        if line: key_points.append(line)

    if not summary or not key_points: return {}
    return {"summary": summary, "key_points": key_points}


PLACEHOLDER_SUMMARY = "the full combined study note, can span multiple lines and paragraphs"

def parse_synthesis(text: str) -> dict:
    ''' parses a TITLE / SUMMARY text block '''

    if not text: return {}

    title = get_field(text, "TITLE")
    summary = get_multiline_field(text, "SUMMARY", [])

    # strip a leaked placeholder line if the model echoed it verbatim
    lines = summary.splitlines()
    if lines and lines[0].strip().lower().startswith(PLACEHOLDER_SUMMARY):
        summary = "\n".join(lines[1:]).strip()

    if not title or not summary: return {}
    return {"title": title, "summary": summary}


def parse_flashcards(text: str) -> list[dict]:
    ''' parses one or more CARD ... ENDCARD blocks '''
    if not text: return []

    cards = []
    for block in re.findall(r'CARD\s*(.*?)\s*ENDCARD', text, re.IGNORECASE | re.DOTALL):

        title = get_field(block, "TITLE")
        front = get_multiline_field(block, "FRONT", ["BACK"])
        back = get_multiline_field(block, "BACK", [])

        if title and front and back:
            cards.append({"title": title, "front": front, "back": back})

    return cards


def parse_quiz(text: str) -> list[dict]:
    ''' parses one or more QUESTION ... ENDQUESTION blocks '''
    if not text: return []

    questions = []
    for block in re.findall(r'QUESTION\s*(.*?)\s*ENDQUESTION', text, re.IGNORECASE | re.DOTALL):
        title = get_field(block, "TITLE")
        question_text = get_multiline_field(block, "TEXT", ["OPTION1"])

        options = [get_field(block, f"OPTION{n}") for n in range(1, 5)]
        options = [o for o in options if o]

        correct_raw = get_field(block, "CORRECT")
        explanation = get_multiline_field(block, "EXPLANATION", [])

        if not (title and question_text and len(options) == 4 and correct_raw and explanation): continue

        correct_answer = ""
        if correct_raw.strip().isdigit():
            index = int(correct_raw.strip()) - 1
            if 0 <= index < len(options): correct_answer = options[index]

        if correct_answer:
            questions.append({
                "title": title, "question": question_text, "options": options,
                "correct_answer": correct_answer, "explanation": explanation})

    return questions
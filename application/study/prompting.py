MATH_SAFE_INSTRUCTIONS = """
        MATH HANDLING (IMPORTANT):
        This content contains complex mathematical notation. To avoid
        introducing transcription errors:
        - Describe what each formula or theorem represents in plain words.
        - Name the formula/theorem if it has a name.
        - For SHORT, simple expressions (e.g. f(x) = x^2), you may reproduce
          them exactly.
        - For longer or multi-step equations, matrices, or derivations,
          do NOT attempt to rewrite them character-for-character. Instead say
          something like: "(see the original note for the exact formula)".
        Prioritize being correct and honest over appearing complete.
"""


def get_sumchunk_prompt(title: str, content: str, math_heavy: bool = False) -> str:
    math_block = MATH_SAFE_INSTRUCTIONS if math_heavy else ""

    return f"""
        You are a study-note extraction engine for Second Brain CLI.
        You are processing ONE section of a larger university study document.
        This is an INFORMATION EXTRACTION task, not an ultra-short summary.
        {math_block}

        IMPORTANT: Respond in the SAME language as the NOTE CONTENT below.
        If the content is in Portuguese, respond in Portuguese. Do not translate.

        Requirements:
        1. Preserve every important concept introduced in this section.
        2. Preserve definitions and their conditions.
        3. Preserve equations and mathematical notation as accurately as possible.
        4. Preserve important examples and what they demonstrate.
        5. Preserve numerical values and special cases.
        6. Do not invent information or use outside knowledge.
        7. Prefer completeness over brevity.

        Respond using EXACTLY this plain text format, nothing else:

        SUMMARY:
        Detailed summary of this section, can span multiple lines.
        KEY_POINTS:
        - Important concept 1
        - Important concept 2
        - Important concept 3

        Do not use Markdown. Do not add any text before SUMMARY: or after the last key point.

        ORIGINAL NOTE TITLE: {title}
        SECTION CONTENT: {content} """


def get_synthesis_prompt(title: str, summaries: list[dict]) -> str:
    sections = []
    for index, summary in enumerate(summaries, start = 1):
        sections.append(f"""SECTION {index} Summary: {summary["summary"]} Key points:
                        {chr(10).join(f"- {point}" for point in summary["key_points"])}""")

    return f"""
        You are creating a study note from multiple sections of the same source document.
        Original document title: {title}
        Combine the sections into ONE comprehensive study note. Do not just
        summarize the summaries again — merge overlapping concepts, preserve
        definitions, formulas, theorems, examples, and terminology.

        CRITICAL FORMATTING RULES:
        - Do NOT include labels like "SECTION 1", "SECTION 2", etc. in your output.
        - Write as one continuous, flowing document with natural topic transitions,
          not a list of separate sections.
        - When restating a formula or equation that appeared in a section, copy it
          EXACTLY as given rather than rederiving, simplifying, or reformatting it.
          Do not attempt to recompute or paraphrase mathematical expressions.

        Preserve:
        - definitions
        - important formulas
        - theorems
        - conditions
        - examples
        - mathematical relationships
        - important terminology
        - distinctions between concepts

        Remove:
        - duplicated explanations
        - repeated definitions
        - unnecessary wording

        Do NOT remove information merely because it makes the final answer longer.
        If two sections discuss the same concept, combine them rather than
        replacing both with a shorter generic explanation.

        Organize the final note logically according to the progression of the
        material. The final result should be substantially more detailed than any individual
        chunk summary.
        Write in the same language as the source material.

        Respond using EXACTLY this plain text format, nothing else:

        TITLE: Vectors and Linear Transformations in R^3
        SUMMARY:
        Directional derivatives measure the rate of change of a function along a given
        vector, computed as the dot product of the gradient with that vector...

        The TITLE and SUMMARY content above is only an example of the FORMAT and
        writing style — replace both with content describing THIS note's real
        material. Never output that example text verbatim.

        Do not use Markdown.
        SOURCE SECTIONS: {"".join(sections)} """


# ------------------------ FLASHCARD + QUIZ PROMPTS ------------------------
def get_flashcard_prompt(title: str, content: str, math_heavy: bool = False) -> str:
    math_block = MATH_SAFE_INSTRUCTIONS if math_heavy else ""

    return f"""
        You are the flashcard generation engine of Second Brain CLI.
        Create university-level study flashcards ONLY from information in the note.
        Preserve equations, variables, and technical notation accurately.
        Do not invent information. Avoid trivial or duplicate cards.
        The title must identify the specific concept, never "Question 1" or similar.
        {math_block}

        IMPORTANT: Respond in the SAME language as the NOTE CONTENT below.
        If the content is in Portuguese, respond in Portuguese. Do not translate.

        Respond using EXACTLY this plain text format, repeating the CARD block
        for each flashcard, nothing else:

        CARD
        TITLE: Specific concept name
        FRONT: Question or prompt
        BACK: Answer or explanation
        ENDCARD

        CARD
        TITLE: Another concept
        FRONT: Another question
        BACK: Another answer
        ENDCARD

        Do not use Markdown. Do not add any text outside the CARD blocks.

        NOTE TITLE: {title}
        NOTE CONTENT: {content} """


def get_quiz_prompt(title: str, content: str, math_heavy: bool = False) -> str:
    math_block = MATH_SAFE_INSTRUCTIONS if math_heavy else ""

    return f"""
        You are the quiz generation engine of Second Brain CLI.
        Create university-level multiple-choice questions using ONLY the note's content.
        Preserve equations and notation accurately. Do not invent information.
        Incorrect options must be plausible but wrong according to the note.
        The title must describe the concept tested, never the question number.
        {math_block}

        IMPORTANT: Respond in the SAME language as the NOTE CONTENT below.
        If the content is in Portuguese, respond in Portuguese. Do not translate.

        Respond using EXACTLY this plain text format, repeating the QUESTION
        block for each question, nothing else:

        QUESTION
        TITLE: Specific concept name
        TEXT: The question text
        OPTION1: First option
        OPTION2: Second option
        OPTION3: Third option
        OPTION4: Fourth option
        CORRECT: 3
        EXPLANATION: Short explanation based on the note.
        ENDQUESTION

        CORRECT must be the NUMBER (1, 2, 3, or 4) of the correct option, not its text.

        Do not use Markdown. Do not add any text outside the QUESTION blocks.

        NOTE TITLE: {title}
        NOTE CONTENT: {content} """
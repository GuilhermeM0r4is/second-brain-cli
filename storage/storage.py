from storage.db import get_connection
from material.model import Note
from ai.model import FlashCard, Quiz, QuizQuestion


def resolve_row(conn, table: str, identifier: str) -> dict | None:
    ''' looks up a single row by id (if numeric) or by exact title, in any table '''

    if identifier.isdigit():
        return conn.execute(f"SELECT * FROM {table} WHERE id = ?", (int(identifier),)).fetchone()
    return conn.execute(f"SELECT * FROM {table} WHERE title = ?", (identifier,)).fetchone()


# ------------------- SETTINGS FUNCTIONS -------------------
def load_settings() -> dict:
    ''' loads the current settings row '''

    with get_connection() as conn:
        row = conn.execute("SELECT * FROM settings WHERE id = 1").fetchone()

    return dict(row) if row else {}


def update_settings(**fields) -> None:
    ''' updates one or more settings columns at once, allows the usage
     of the function to be free (update_settings(dpi=150)) or even use
     update_settings(ai_provider="anthropic", ai_model="claude-sonnet-5")'''

    if not fields: return   # nothing was passed in, nothing to do

    allowed_columns = {"dpi", "usr_language", "ai_provider", "ai_model", "api_key", "data_sharing"}
    invalid = set(fields) - allowed_columns

    if invalid:
        raise ValueError(f"Unknown settings field(s): {invalid}")

    # creates the clause to set using each given info in the fields
    set_clause = ", ".join(f"{column} = ?" for column in fields)
    values = list(fields.values())

    with get_connection() as conn:
        conn.execute(f"UPDATE settings SET {set_clause} WHERE id = 1", values)
        conn.commit()


# ------------------- NOTES FUNCTIONS -------------------
def add_note(note: Note) -> None:
    ''' adds a note to the database '''

    with get_connection() as conn:
        conn.execute(   # inserts a note into the database
            "INSERT INTO notes (title, content, favorite, created_at) VALUES (?, ?, ?, ?)",
            (note.title, note.content, note.favorite, note.created_at))
    
        conn.commit()


def load_notes() -> list[Note]:
    ''' loads all notes from the database '''

    conn = get_connection()
    rows = conn.execute("SELECT * FROM notes ORDER BY created_at DESC").fetchall()
    conn.close()

    return [Note(id=row["id"], title=row["title"], content=row["content"],
                 tags="", favorite=row["favorite"], created_at=row["created_at"]) for row in rows]


def find_note(identifier: str) -> Note | None:
    ''' finds a note by id (if numeric) or by exact title '''

    conn = get_connection()
    row = resolve_row(conn, "notes", identifier)
    conn.close()

    if row is None: return None
    return Note(id=row["id"], title=row["title"], content=row["content"],
                tags="", favorite=row["favorite"], created_at=row["created_at"])


def update_note(identifier: str, title: str, content: str, favorite: str) -> None:
    ''' updates a note found by id or title '''

    note = find_note(identifier)
    # nothing found, nothing to update — caller can check and print an error
    if note is None: return

    with get_connection() as conn:
        conn.execute("UPDATE notes SET title = ?, content = ?, favorite = ? WHERE id = ?", (title, content, favorite, note.id))
        conn.commit()


def delete_note(identifier: str) -> bool:
    ''' deletes a note found by id or title '''

    note = find_note(identifier)
    if note is None: return False

    with get_connection() as conn:
        conn.execute("DELETE FROM notes WHERE id = ?", (note.id,))
        conn.commit()

    return True


# ------------------- FLASHCARDS FUNCTIONS -------------------
def add_flashcard(card: FlashCard) -> None:
    ''' adds a flashcard to the database '''

    with get_connection() as conn:
        conn.execute(
            "INSERT INTO flashcards (title, front, back, favorite, created_at) VALUES (?, ?, ?, ?, ?)",
            (card.title, card.front, card.back, card.favorite, card.created_at))
    
        conn.commit()


def load_flashcards() -> list[FlashCard]:
    ''' loads all flashcards from the database '''

    with get_connection() as conn:
    # pulls back all matching rows and uses the first match
        rows = conn.execute("SELECT * FROM flashcards ORDER BY created_at DESC").fetchall()

    return [FlashCard(id=row["id"], title=row["title"], front=row["front"], back=row["back"],
                 favorite=row["favorite"], created_at=row["created_at"]) for row in rows]


def find_flashcard(identifier: str) -> FlashCard | None:
    ''' finds a flashcard by id (if numeric) or by exact title '''

    with get_connection() as conn:
        row = resolve_row(conn, "flashcards", identifier)

    if row is None: return None

    return FlashCard(id=row["id"], title=row["title"], front=row["front"], back=row["back"],
                    favorite=row["favorite"], created_at=row["created_at"])


def update_flashcard(identifier: str, title: str, front: str, back: str) -> None:
    ''' updates a flashcard found by id or title '''

    card = find_flashcard(identifier)
    # nothing found, nothing to update — caller can check and print an error
    if card is None: return

    with get_connection() as conn:
        conn.execute("UPDATE flashcards SET title = ?, front = ?, back = ? WHERE id = ?", (title, front, back, card.id))
        conn.commit()


def delete_flashcard(identifier: str) -> bool:
    ''' deletes a flashcard found by id or title '''

    card = find_flashcard(identifier)
    if card is None: return False

    with get_connection() as conn:
        conn.execute("DELETE FROM flashcards WHERE id = ?", (card.id,))
        conn.commit()

    return True


# ------------------- QUIZZES FUNCTIONS -------------------
def add_quiz(quiz: Quiz) -> None:
    ''' adds a quiz and all its questions to the database '''

    with get_connection() as conn:
        # insert the quiz itself, and capture the id SQLite just generated
        cursor = conn.execute("INSERT INTO quizzes (title, favorite, created_at) VALUES (?, ?, ?)",
                            (quiz.title, quiz.favorite, quiz.created_at))

        quiz_id = cursor.lastrowid # gets the id from quiz

        # build one tuple per question, tagging each with the new quiz_id
        question_rows = [(quiz_id, q.question, q.option1, q.option2, q.option3, q.option4,
                        q.correct_answer, q.explanation) for q in quiz.questions]

        conn.executemany(   # insert all questions in one batch
            """INSERT INTO quiz_questions
            (quiz_id, question, option1, option2, option3, option4, correct_answer, explanation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", question_rows)

        conn.commit()


def load_quizzes() -> list[Quiz]:
    """ loads all quizzes from the database """

    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM quizzes ORDER BY created_at DESC").fetchall()

    return [Quiz(id=row["id"], title=row["title"], favorite=row["favorite"],
            created_at=row["created_at"], questions=[]) for row in rows]


def load_quiz(identifier: str) -> Quiz | None:
    ''' loads a full quiz (with all its questions) by id or title '''

    with get_connection() as conn:
        quiz_row = resolve_row(conn, "quizzes", identifier)

        if quiz_row is None:
            conn.close()
            return None

        question_rows = conn.execute(
            "SELECT * FROM quiz_questions WHERE quiz_id = ?", (quiz_row["id"],)).fetchall()

    questions = [QuizQuestion(id=row["id"], question=row["question"],
                               option1=row["option1"], option2=row["option2"],
                               option3=row["option3"], option4=row["option4"],
                               correct_answer=row["correct_answer"],
                               explanation=row["explanation"]) for row in question_rows]

    return Quiz(id=quiz_row["id"], title=quiz_row["title"], favorite=quiz_row["favorite"],
                created_at=quiz_row["created_at"], questions=questions)


def find_quiz(identifier: str) -> Quiz | None:
    ''' finds a quiz's own row (without questions) by id or title '''

    with get_connection() as conn:
        row = resolve_row(conn, "quizzes", identifier)

    if row is None: return None

    return Quiz(id=row["id"], title=row["title"], favorite=row["favorite"],
                created_at=row["created_at"], questions=[])


def update_quiz(identifier: str, title: str) -> None:
    ''' updates a quiz's title, found by id or title '''

    quiz = find_quiz(identifier)
    if quiz is None: return

    with get_connection() as conn:
        conn.execute("UPDATE quizzes SET title = ? WHERE id = ?", (title, quiz.id))
        conn.commit()


def delete_quiz(identifier: str) -> bool:
    ''' deletes a quiz and all its questions, found by id or title '''

    quiz = find_quiz(identifier)
    if quiz is None: return False

    with get_connection() as conn:
        conn.execute("DELETE FROM quiz_questions WHERE quiz_id = ?", (quiz.id,))  # children first
        conn.execute("DELETE FROM quizzes WHERE id = ?", (quiz.id,))              # then the parent
        conn.commit()

    return True
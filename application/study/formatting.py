from application.study.model import FlashCard, Quiz

from application.material.config import CONSOLE

from rich.panel import Panel


def format_card_print(card: FlashCard) -> None:
    """ formats the print output to give the flashcards info """

    print()
    CONSOLE.print(      # displays the summary in a panel
        Panel(
            f"[cyan]ID: [/cyan]{card.id}\n"
            f"[cyan]Front: [/cyan]{card.front}\n\n"
            f"[cyan]Back: [/cyan]{card.back}",
            border_style = "cyan", 
            title = f"{card.title}",
        ), width = 100
    )


def format_quiz_print(quiz: Quiz) -> None:
    """ formats the print output to give the quizzes info """

    quiz_question = quiz.questions[0]  # uses a list[QuizQuestion]
    print()
    opt_text = f"{quiz_question.option1}\n{quiz_question.option2}\n{quiz_question.option3}\n{quiz_question.option4}"
    
    CONSOLE.print(      # displays the summary in a panel
        Panel(
            f"[cyan]ID: [/cyan]{quiz.id}\n\n"
            f"[cyan]Q: [/cyan]{quiz_question.question}\n"
            f"{opt_text}\n\n\n\n"
            f"[cyan]A: [/cyan]{quiz_question.correct_answer}\n"
            f"[cyan]Exp: [/cyan]{quiz_question.explanation}",
            border_style = "cyan", 
            title = f"{quiz.title}",
        ), width = 100
    )
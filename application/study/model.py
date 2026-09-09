from dataclasses import dataclass

@dataclass
class Model:
    provider: str | None = "ollama"
    model: str | None = "NONE"
    api_key: str | None = "NONE"
    data_sharing: str | None = "LOCAL"  # default value for data sharing

@dataclass
class FlashCard:
    id: int
    title: str
    front: str
    back: str
    favorite: int
    created_at: str

@dataclass
class QuizQuestion:
    id: int
    question: str
    option1: str
    option2: str
    option3: str
    option4: str
    correct_answer: str
    explanation: str

@dataclass
class Quiz:
    id: int
    title: str
    favorite: int
    created_at: str
    questions: list[QuizQuestion]
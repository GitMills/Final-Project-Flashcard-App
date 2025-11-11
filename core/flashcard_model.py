# FINAL PROJECT FLASHCARD APP / core / flashcard_model.py

from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Flashcard:
    question: str
    answer: str
    custom_hint: str = None

@dataclass  
class FlashcardSet:
    set_name: str
    cards: List[Flashcard]
    created_date: str = None
    
    def __post_init__(self):
        if self.created_date is None:
            self.created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@dataclass
class StudyProgress:
    learned: bool = False
    times_correct: int = 0
    times_wrong: int = 0

@dataclass
class StudyFlashcard(Flashcard):
    progress: StudyProgress = None
    
    def __post_init__(self):
        if self.progress is None:
            self.progress = StudyProgress()
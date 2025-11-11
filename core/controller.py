# FINAL PROJECT FLASHCARD APP / core / controller.py

from typing import List, Dict
from .data_manager import DataManager
from .flashcard_model import Flashcard, FlashcardSet

class FlashcardController:
    def __init__(self):
        # Initialize data manager for file operations
        self.data_manager = DataManager()
    
    def create_flashcard_set(self, set_name: str, cards_data: List[Dict], difficulty: str = 'Easy') -> str:
        # Validate set name
        if not set_name.strip():
            return "Set name cannot be empty"
        
        # Validate at least one card exists
        if not cards_data:
            return "At least one flashcard required"
        
        # Convert dictionary data to Flashcard objects with custom hints
        flashcards = []
        for q in cards_data:
            card = Flashcard(q['question'], q['answer'])
            if 'custom_hint' in q:
                card.custom_hint = q['custom_hint']
            flashcards.append(card)
        
        # Create flashcard set with difficulty
        flashcard_set = FlashcardSet(set_name, flashcards)
        flashcard_set.difficulty = difficulty
        
        # Save to file and return result
        if self.data_manager.save_flashcard_set(flashcard_set):
            return ""  # Empty string means success
        else:
            return "Failed to save flashcard set"
    
    def get_all_sets(self) -> List[Dict]:
        # Return all flashcard sets as dictionaries
        return self.data_manager.load_all_sets_dict()
    
    def get_study_set(self, set_name: str):
        """Get a set with study progress data"""
        all_sets = self.data_manager.load_all_sets_dict()
        for flashcard_set in all_sets:
            if flashcard_set['set_name'] == set_name:
                return flashcard_set
        return None

    def update_card_progress(self, set_name: str, card_index: int, learned: bool, correct: bool):
        """Update study progress for a card"""
        return self.data_manager.update_study_progress(set_name, card_index, learned, correct)


    def delete_flashcard_set(self, set_name: str) -> str:
        """Delete a flashcard set - returns empty string if success, error message if failed"""
        if not set_name.strip():
            return "Set name cannot be empty"
        
        if self.data_manager.delete_flashcard_set(set_name):
            return ""
        else:
            return "Failed to delete flashcard set"
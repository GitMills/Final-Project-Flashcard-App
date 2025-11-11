# FINAL PROJECT FLASHCARD APP / core / data_manager.py


import json
import os
from typing import List, Dict
from .flashcard_model import FlashcardSet, Flashcard

class DataManager:
    def __init__(self):
        self.data_dir = "data"
        self.data_file = os.path.join(self.data_dir, "flashcard_sets.json")
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
    
    def save_flashcard_set(self, flashcard_set: FlashcardSet) -> bool:
        try:
            # Read existing sets from file
            all_sets = self.load_all_sets_dict()
            
            # Convert flashcard set to dictionary format
            set_data = {
                'set_name': flashcard_set.set_name,
                'created_date': flashcard_set.created_date,
                'cards': []
            }
            
            # Add difficulty if exists
            if hasattr(flashcard_set, 'difficulty'):
                set_data['difficulty'] = flashcard_set.difficulty
            
            # Add cards with custom hints if they exist
            for card in flashcard_set.cards:
                card_data = {'question': card.question, 'answer': card.answer}
                if hasattr(card, 'custom_hint') and card.custom_hint:
                    card_data['custom_hint'] = card.custom_hint
                set_data['cards'].append(card_data)
            
            # Add new set to existing sets
            all_sets.append(set_data)
            
            # Write all sets back to JSON file
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(all_sets, f, indent=4, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Save error: {e}")
            return False
    
    def load_all_sets_dict(self) -> List[Dict]:
        # Return empty list if file doesn't exist
        if not os.path.exists(self.data_file):
            return []
        
        try:
            # Load and return all sets from JSON file
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            # Return empty list if file is corrupted
            return []

    def _save_all_sets(self, all_sets):
        """Save all flashcard sets to the JSON file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(all_sets, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving flashcard sets: {e}")
            return False

    def update_study_progress(self, set_name: str, card_index: int, learned: bool, correct: bool):
        """Update progress for a specific card in a set"""
        try:
            
            all_sets = self.load_all_sets_dict()
            
            for flashcard_set in all_sets:
                if flashcard_set['set_name'] == set_name:
                    
                    if card_index >= len(flashcard_set['cards']):
                        return False
                    
                    if 'progress' not in flashcard_set['cards'][card_index]:
                        flashcard_set['cards'][card_index]['progress'] = {
                            'learned': False,
                            'times_correct': 0,
                            'times_wrong': 0
                        }
                    
                    if correct:
                        flashcard_set['cards'][card_index]['progress']['times_correct'] += 1
                    else:
                        flashcard_set['cards'][card_index]['progress']['times_wrong'] += 1
                    
                    flashcard_set['cards'][card_index]['progress']['learned'] = learned
                    
                    self._save_all_sets(all_sets)
                    return True
            
            return False
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return False


    def delete_flashcard_set(self, set_name: str) -> bool:
        """Delete a flashcard set by name"""
        try:
            all_sets = self.load_all_sets_dict()
            
            # Find and remove the set
            for i, flashcard_set in enumerate(all_sets):
                if flashcard_set['set_name'] == set_name:
                    all_sets.pop(i)
                    self._save_all_sets(all_sets)
                    return True
            return False
        except Exception as e:
            print(f"Delete error: {e}")
            return False
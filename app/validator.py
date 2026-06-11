from typing import List
from .models import FinalActionItem, Phase3Output

class Validator:
    @staticmethod
    def validate_action(item: FinalActionItem) -> bool:
        if not item.title or not item.title.strip():
            return False
            
        # Basic check for actionability (e.g., must be more than one word)
        words = item.title.strip().split()
        if len(words) < 2:
            return False
            
        if not item.description or not item.description.strip():
            return False
            
        return True

    @staticmethod
    def validate_output(output: Phase3Output) -> Phase3Output:
        valid_actions = []
        for action in output.actions:
            if Validator.validate_action(action):
                valid_actions.append(action)
                
        output.actions = valid_actions
        output.final_action_items = len(valid_actions)
        return output

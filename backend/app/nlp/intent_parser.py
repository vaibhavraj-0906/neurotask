"""
Intent Parser - Determines user's intent from raw text
"""

import re
from enum import Enum
from typing import Dict, Optional, Tuple


class Intent(str, Enum):
    """Intent types"""
    CREATE_TASK = "create_task"
    EDIT_TASK = "edit_task"
    DELETE_TASK = "delete_task"
    COMPLETE_TASK = "complete_task"
    LIST_TASKS = "list_tasks"
    SEARCH_TASKS = "search_tasks"
    UNKNOWN = "unknown"


class IntentParser:
    """Parse user input to determine intent"""
    
    # Intent patterns
    INTENT_PATTERNS = {
        Intent.DELETE_TASK: [
            r"delete\s+(?:the\s+)?(.+?)(?:\s+task)?$",
            r"remove\s+(?:the\s+)?(.+?)(?:\s+task)?$",
            r"forget\s+(?:about\s+)?(.+)",
            r"(?:the\s+)?(.+?)\s+(?:task\s+)?(?:is\s+)?gone",
        ],
        Intent.COMPLETE_TASK: [
            r"(?:mark\s+)?(?:complete|done|finish)(?:ed)?\s+(?:the\s+)?(.+?)(?:\s+task)?$",
            r"(?:the\s+)?(.+?)\s+(?:is\s+)?(?:done|complete)",
            r"finished\s+(?:the\s+)?(.+)",
            r"completed\s+(?:the\s+)?(.+)",
        ],
        Intent.EDIT_TASK: [
            r"(?:move|change|reschedule|set|update)\s+(?:the\s+)?(.+?)\s+(?:to|at)\s+(.+)",
            r"(?:the\s+)?(.+?)\s+(?:to|should be)\s+(.+)",
            r"remind\s+me\s+(.+?)\s+(?:in|at)\s+(.+)",
        ],
        Intent.SEARCH_TASKS: [
            r"(?:show|find|search|look for|find all)\s+(?:my\s+)?(.+?)(?:\s+tasks)?$",
            r"what\s+(?:are\s+)?my\s+(.+?)\s+(?:tasks)?",
            r"list\s+(?:all\s+)?(?:my\s+)?(.+?)(?:\s+tasks)?",
        ],
        Intent.LIST_TASKS: [
            r"^(?:show|list|display|what|tell me)\s+(?:my\s+)?(?:all\s+)?(?:tasks|todo)",
            r"^(?:what|show|list)\s+(?:do\s+)?i\s+(?:have\s+)?(?:to\s+)?(?:do|work on)",
            r"^my\s+(?:tasks|todos|agenda)",
        ],
    }
    
    def parse(self, text: str) -> Tuple[Intent, Optional[str], float]:
        """
        Parse user input and determine intent
        
        Args:
            text: User input text
            
        Returns:
            Tuple of (intent, extracted_info, confidence_score)
        """
        text = text.strip().lower()
        
        # Check each intent pattern
        for intent, patterns in self.INTENT_PATTERNS.items():
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    extracted_info = match.group(1) if match.groups() else None
                    confidence = 0.9  # High confidence for pattern matching
                    return intent, extracted_info, confidence
        
        # If no specific intent matched, it's likely a create_task intent
        # (default behavior when user just types a task description)
        return Intent.CREATE_TASK, text, 0.7
    
    def get_intent(self, text: str) -> Intent:
        """Get intent from text"""
        intent, _, _ = self.parse(text)
        return intent
    
    def get_extracted_info(self, text: str) -> Optional[str]:
        """Get extracted info from text"""
        _, info, _ = self.parse(text)
        return info
    
    def get_confidence(self, text: str) -> float:
        """Get confidence score for intent parsing"""
        _, _, confidence = self.parse(text)
        return confidence

"""
Main NLP Engine - Combines intent parsing and entity extraction
"""

from typing import Dict, Any, Optional
from app.nlp.intent_parser import IntentParser, Intent
from app.nlp.entity_extractor import EntityExtractor


class NLPEngine:
    """Main NLP engine for task parsing"""
    
    def __init__(self):
        self.intent_parser = IntentParser()
        self.entity_extractor = EntityExtractor()
    
    def parse(self, text: str) -> Dict[str, Any]:
        """
        Parse natural language input into structured task data
        
        Args:
            text: Raw user input
            
        Returns:
            Structured parsing result
        """
        # Parse intent
        intent, extracted_info, intent_confidence = self.intent_parser.parse(text)
        
        # Extract entities
        entities = self.entity_extractor.extract(text)
        
        # Build response
        result = {
            "raw_input": text,
            "intent": intent.value,
            "intent_confidence": intent_confidence,
            "task_title": entities.get("task_title", ""),
            "deadline": entities.get("datetime"),
            "reminder_time": entities.get("datetime"),
            "priority": entities.get("priority", "medium"),
            "category": entities.get("category"),
            "recurrence": entities.get("recurrence"),
            "confidence_score": entities.get("confidence", 50),
            "parsed_at": self._get_current_timestamp(),
        }
        
        return result
    
    @staticmethod
    def _get_current_timestamp() -> str:
        """Get current timestamp in ISO format"""
        from datetime import datetime
        return datetime.utcnow().isoformat()

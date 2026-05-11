"""
Entity Extractor - Extracts structured entities from natural language
"""

import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import dateparser
import pytz

from app.config import TIMEZONE, CONFIDENCE_THRESHOLD


class EntityExtractor:
    """Extract entities from text"""
    
    # Priority keywords mapping
    PRIORITY_KEYWORDS = {
        "high": ["urgent", "asap", "immediately", "critical", "important", "priority"],
        "medium": ["need to", "should", "tonight", "soon", "this week"],
        "low": ["maybe", "someday", "whenever", "later", "can wait"],
    }
    
    # Category keywords
    CATEGORY_KEYWORDS = {
        "study": ["assignment", "project", "homework", "study", "exam", "test", "lecture", "reading", "lab", "report", "paper", "essay"],
        "fitness": ["gym", "exercise", "workout", "run", "jog", "yoga", "swimming", "sports", "cycling"],
        "work": ["meeting", "presentation", "report", "deadline", "client", "email", "call", "conference"],
        "personal": ["call", "visit", "meet", "talk to", "mom", "dad", "friend", "family", "birthday"],
        "finance": ["pay", "bill", "fee", "invoice", "tax", "loan", "mortgage", "transfer", "bank"],
        "shopping": ["buy", "purchase", "groceries", "shopping", "store", "shop"],
        "entertainment": ["watch", "movie", "game", "play", "read", "book", "netflix", "show"],
    }
    
    # Time expressions for recurrence
    RECURRENCE_PATTERNS = {
        "daily": ["every day", "daily", "each day"],
        "weekdays": ["every weekday", "weekdays", "monday to friday", "mon-fri"],
        "weekends": ["every weekend", "weekends", "saturday and sunday"],
        "weekly": ["every week", "weekly"],
        "biweekly": ["every two weeks", "every other week", "biweekly"],
    }
    
    def __init__(self):
        self.timezone = pytz.timezone(TIMEZONE)
    
    def extract(self, text: str) -> Dict[str, Any]:
        """
        Extract all entities from text
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with extracted entities
        """
        result = {
            "task_title": self._extract_task_title(text),
            "datetime": self._extract_datetime(text),
            "priority": self._extract_priority(text),
            "category": self._extract_category(text),
            "recurrence": self._extract_recurrence(text),
            "confidence": self._calculate_confidence(text),
        }
        return result
    
    def _extract_task_title(self, text: str) -> str:
        """Extract task title by removing date/time references"""
        # Remove time expressions
        cleaned = re.sub(
            r"\b(tomorrow|tonight|today|this|next|last|in \d+ (?:hours?|minutes?|days?)|at \d+(?::\d+)?|morning|afternoon|evening|night|asap|urgent|soon|later|maybe|someday)\b",
            "",
            text,
            flags=re.IGNORECASE
        )
        
        # Remove extra whitespace and return
        title = re.sub(r"\s+", " ", cleaned).strip()
        
        # If title is too short or empty, use original text
        if len(title) < 3:
            return text[:100]
        
        return title[:500]
    
    def _extract_datetime(self, text: str) -> Optional[str]:
        """
        Extract date and time from text
        
        Returns ISO format datetime string or None
        """
        # Try common time expressions
        time_patterns = {
            r"tomorrow": lambda: (datetime.now(self.timezone) + timedelta(days=1)).replace(hour=21, minute=0),
            r"tonight": lambda: datetime.now(self.timezone).replace(hour=21, minute=0),
            r"today": lambda: datetime.now(self.timezone),
            r"in\s+(\d+)\s+hours?": lambda m: datetime.now(self.timezone) + timedelta(hours=int(m.group(1))),
            r"in\s+(\d+)\s+minutes?": lambda m: datetime.now(self.timezone) + timedelta(minutes=int(m.group(1))),
            r"in\s+(\d+)\s+days?": lambda m: datetime.now(self.timezone) + timedelta(days=int(m.group(1))),
        }
        
        for pattern, func in time_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    dt = func(match) if callable(func) and match.groups() else func()
                    return dt.isoformat()
                except:
                    pass
        
        # Try dateparser as fallback
        try:
            parsed = dateparser.parse(
                text,
                settings={"TIMEZONE": TIMEZONE, "RETURN_AS_TIMEZONE_AWARE": True}
            )
            if parsed:
                return parsed.isoformat()
        except:
            pass
        
        return None
    
    def _extract_priority(self, text: str) -> str:
        """
        Detect priority from keywords in text
        
        Returns: "high", "medium", or "low"
        """
        text_lower = text.lower()
        
        # Check high priority keywords
        for keyword in self.PRIORITY_KEYWORDS["high"]:
            if keyword in text_lower:
                return "high"
        
        # Check low priority keywords
        for keyword in self.PRIORITY_KEYWORDS["low"]:
            if keyword in text_lower:
                return "low"
        
        # Check medium priority keywords
        for keyword in self.PRIORITY_KEYWORDS["medium"]:
            if keyword in text_lower:
                return "medium"
        
        # Default
        return "medium"
    
    def _extract_category(self, text: str) -> Optional[str]:
        """
        Auto-detect category from keywords
        """
        text_lower = text.lower()
        
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return category
        
        return None
    
    def _extract_recurrence(self, text: str) -> Optional[str]:
        """
        Extract recurrence pattern
        """
        text_lower = text.lower()
        
        # Check for specific day recurrence
        days = {
            "monday": "MO", "tuesday": "TU", "wednesday": "WE",
            "thursday": "TH", "friday": "FR", "saturday": "SA", "sunday": "SU"
        }
        
        found_days = []
        for day_name, day_code in days.items():
            if day_name in text_lower or day_name[:3] in text_lower:
                found_days.append(day_code)
        
        if found_days and any(word in text_lower for word in ["every", "each"]):
            return f"FREQ=WEEKLY;BYDAY={','.join(found_days)}"
        
        # Check recurrence patterns
        for recurrence, patterns in self.RECURRENCE_PATTERNS.items():
            for pattern in patterns:
                if pattern in text_lower:
                    return f"FREQ={recurrence.upper()}"
        
        return None
    
    def _calculate_confidence(self, text: str) -> int:
        """
        Calculate confidence score (0-100)
        Based on clarity and completeness of extraction
        """
        score = 50  # Base score
        
        # Add points for presence of useful entities
        if self._extract_datetime(text):
            score += 20
        if self._extract_category(text):
            score += 15
        if self._extract_recurrence(text):
            score += 10
        
        # Reduce if text is too short or vague
        if len(text) < 5:
            score -= 20
        
        # Cap at 100
        return min(score, 100)

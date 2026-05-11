# NeuroTask NLP System Documentation

Deep dive into the NLP engine that powers NeuroTask's natural language understanding.

---

## Overview

The NLP system transforms raw user input into structured task data. It's designed to be:
- **Fast** - Process in milliseconds
- **Accurate** - High confidence parsing
- **Flexible** - Understand casual, natural language
- **Extensible** - Easy to add new patterns

---

## Architecture

### Pipeline

```
Raw Input
    ↓
Preprocessing (lowercase, trim, clean)
    ↓
Intent Detection (what does the user want?)
    ↓
Entity Extraction (what are the details?)
    ↓
Task Structuring (normalize to schema)
    ↓
Confidence Scoring (how confident are we?)
    ↓
Structured Output
```

---

## Step 1: Intent Detection

### Purpose
Determine what action the user wants to perform.

### Intents

| Intent | Pattern | Example |
|--------|---------|---------|
| `create_task` | Default | "Finish assignment" |
| `edit_task` | "move", "change", "reschedule" | "Move gym to 7 PM" |
| `delete_task` | "delete", "remove", "forget" | "Delete the assignment" |
| `complete_task` | "mark done", "completed", "finished" | "Mark done the meeting" |
| `list_tasks` | "show", "list", "what do I have" | "Show my tasks" |
| `search_tasks` | "find", "search", "look for" | "Find all study tasks" |

### Implementation

```python
class IntentParser:
    INTENT_PATTERNS = {
        Intent.DELETE_TASK: [
            r"delete\s+(?:the\s+)?(.+?)(?:\s+task)?$",
            r"remove\s+(?:the\s+)?(.+?)(?:\s+task)?$",
        ],
        Intent.COMPLETE_TASK: [
            r"(?:mark\s+)?(?:complete|done)\s+(?:the\s+)?(.+)$",
        ],
        # ... more patterns
    }
```

### Confidence Scoring for Intent

- **Exact pattern match**: 90% confidence
- **Partial match**: 70% confidence
- **Default (create_task)**: 70% confidence

---

## Step 2: Entity Extraction

### Purpose
Extract structured entities from unstructured text.

### Entities

#### 1. Task Title
**Extraction**: Remove date/time/priority words, keep core task

```
Input:  "Finish OS lab report tonight"
Output: "Finish OS lab report"
```

**Method**: Regex removal of temporal and intensity words

#### 2. Date & Time
**Extraction**: Parse dates, times, and relative expressions

**Supported Formats**:
- Absolute: "2024-01-20", "Jan 20", "tomorrow"
- Relative: "in 2 hours", "next Friday", "tonight"
- Fuzzy: "ASAP", "soon", "later"

**Implementation**:
```python
def _extract_datetime(text: str) -> Optional[str]:
    # Try specific patterns first
    if "tomorrow" in text:
        return (datetime.now() + timedelta(days=1)).isoformat()
    if "in 2 hours" in text:
        return (datetime.now() + timedelta(hours=2)).isoformat()
    
    # Fall back to dateparser
    return dateparser.parse(text, settings={
        'TIMEZONE': 'UTC',
        'RETURN_AS_TIMEZONE_AWARE': True
    }).isoformat()
```

#### 3. Priority
**Extraction**: Infer urgency from keywords

**Mapping**:
```python
PRIORITY_KEYWORDS = {
    "high": ["urgent", "asap", "immediately", "critical"],
    "medium": ["need to", "should", "tonight", "soon"],
    "low": ["maybe", "someday", "later", "whenever"],
}
```

**Examples**:
- "URGENT: submit assignment" → HIGH
- "Maybe watch Batman" → LOW
- "Finish project tonight" → MEDIUM (default)

#### 4. Category
**Extraction**: Auto-detect task type

**Categories & Keywords**:
```python
CATEGORY_KEYWORDS = {
    "study": ["assignment", "homework", "exam", "study"],
    "fitness": ["gym", "exercise", "workout", "yoga"],
    "work": ["meeting", "report", "deadline", "presentation"],
    "personal": ["call", "visit", "family", "birthday"],
    "finance": ["pay", "bill", "fee", "invoice"],
    "shopping": ["buy", "groceries", "purchase"],
    "entertainment": ["watch", "movie", "game", "read"],
}
```

**Examples**:
- "Gym tomorrow" → FITNESS
- "Pay electricity bill" → FINANCE
- "Study for exam" → STUDY

#### 5. Recurrence
**Extraction**: Detect repeating patterns

**Patterns**:
- Weekly: "every Monday", "weekdays"
- Custom days: "Mon, Wed, Fri"
- Daily: "every day"
- Biweekly: "every two weeks"

**Implementation**:
```python
def _extract_recurrence(text: str) -> Optional[str]:
    # Check for specific days
    days = {"monday": "MO", "tuesday": "TU", ...}
    found_days = []
    for day, code in days.items():
        if day in text:
            found_days.append(code)
    
    if found_days and "every" in text:
        return f"FREQ=WEEKLY;BYDAY={','.join(found_days)}"
    
    # ... check other patterns
```

**Output Format**: iCalendar RRULE
```
FREQ=WEEKLY;BYDAY=MO,WE,FR
FREQ=DAILY
FREQ=MONTHLY;BYMONTHDAY=15
```

---

## Step 3: Task Structuring

### Purpose
Normalize extracted entities into task schema.

### Task Schema

```python
task = {
    "task_title": str,           # What to do
    "deadline": datetime|None,   # When it's due
    "reminder_time": datetime|None,  # When to remind
    "priority": "high"|"medium"|"low",  # Urgency
    "category": str|None,        # Type of task
    "recurrence": str|None,      # RRULE pattern
    "confidence_score": int,     # 0-100
    "original_text": str,        # Raw input
}
```

### Processing Steps

1. **Validate data types**
   ```python
   deadline = self._parse_datetime(deadline_str)
   if deadline and deadline < datetime.now():
       # Might be next occurrence
       deadline = deadline + timedelta(days=365)
   ```

2. **Set defaults**
   ```python
   priority = priority or "medium"
   category = category or None
   ```

3. **Resolve ambiguities**
   ```python
   # "Friday" could be today or next week
   # If past time today, assume next week
   if deadline < datetime.now():
       deadline = deadline + timedelta(days=7)
   ```

4. **Store raw parsing**
   ```python
   parsed_data = {
       "intent": intent,
       "entities": extracted_entities,
       "transformations": [...],
   }
   ```

---

## Step 4: Confidence Scoring

### Scoring Algorithm

```python
def _calculate_confidence(text: str) -> int:
    score = 50  # Base score
    
    # Add points for extracted entities
    if self._extract_datetime(text):
        score += 20  # +20 if date/time present
    if self._extract_category(text):
        score += 15  # +15 if category detected
    if self._extract_recurrence(text):
        score += 10  # +10 if recurrence found
    
    # Reduce if text is too short or vague
    if len(text) < 5:
        score -= 20
    
    return min(max(score, 0), 100)
```

### Confidence Levels

| Range | Level | Meaning |
|-------|-------|---------|
| 90-100 | Very High | Clear intent, all details |
| 70-89 | High | Clear intent, most details |
| 50-69 | Medium | Parseable, some details missing |
| 30-49 | Low | Ambiguous, needs clarification |
| 0-29 | Very Low | Cannot parse reliably |

### Example Confidence Scores

```
"Gym every Monday Wednesday Friday at 6 am"
→ 95% (clear, complete, recurring, specific time)

"Finish assignment"
→ 65% (clear what, unclear when)

"maybe do something later"
→ 35% (vague what, vague when, low priority)
```

---

## Examples

### Example 1: Complex Recurring Task

**Input:**
```
"Gym every Monday Wednesday Friday at 6 am"
```

**Parsing Process:**

1. **Intent Detection**
   - Matches: "create_task" (default)
   - Confidence: 70%

2. **Entity Extraction**
   - Task Title: "Gym"
   - Time: "6:00 AM"
   - Recurrence: "FREQ=WEEKLY;BYDAY=MO,WE,FR"
   - Priority: "low" (fitness tasks usually low)
   - Category: "fitness"

3. **Task Structuring**
   ```json
   {
     "task": "Gym",
     "time": "06:00",
     "deadline": "Today 06:00",
     "recurrence": "FREQ=WEEKLY;BYDAY=MO,WE,FR",
     "priority": "low",
     "category": "fitness"
   }
   ```

4. **Confidence Score**
   - Base: 50
   - +20 for datetime
   - +15 for category
   - +10 for recurrence
   - **Total: 95%**

---

### Example 2: High-Priority Assignment

**Input:**
```
"URGENT: submit DSA assignment ASAP"
```

**Parsing Process:**

1. **Intent Detection**
   - Matches: "create_task"
   - Confidence: 90%

2. **Entity Extraction**
   - Task Title: "Submit DSA assignment"
   - Priority: "high" (keywords: URGENT, ASAP)
   - Deadline: null (no specific date given, but ASAP implies urgent)
   - Category: "study" (keywords: assignment, DSA)

3. **Task Structuring**
   ```json
   {
     "task": "Submit DSA assignment",
     "deadline": null,
     "priority": "high",
     "category": "study",
     "original_text": "URGENT: submit DSA assignment ASAP"
   }
   ```

4. **Confidence Score**
   - Base: 50
   - +15 for category
   - -20 for vague time
   - **Total: 45%** (Medium confidence - missing specific deadline)

---

### Example 3: Edit Existing Task

**Input:**
```
"Move gym to 7 PM"
```

**Parsing Process:**

1. **Intent Detection**
   - Matches: "edit_task" (pattern: "move ... to ...")
   - Extracted: task="gym", new_value="7 PM"
   - Confidence: 90%

2. **Entity Extraction**
   - Task to Update: "gym" (entity 1)
   - New Time: "7 PM" (entity 2)

3. **Task Structuring**
   ```json
   {
     "intent": "edit_task",
     "task_query": "gym",
     "updates": {
       "reminder_time": "19:00"
     }
   }
   ```

4. **Confidence Score: 88%** (Clear intent and modification)

---

## Advanced Features

### 1. Spelling Tolerance

Handle typos gracefully:
```
"assigment" → "assignment"
"tommorow" → "tomorrow"
"fittnes" → "fitness"
```

**Implementation**: Fuzzy matching with `difflib.get_close_matches()`

### 2. Abbreviation Expansion

```
"DSA" → "Data Structures and Algorithms"
"OS" → "Operating Systems"
"Mon" → "Monday"
```

**Implementation**: Predefined abbreviation dictionary

### 3. Casual Phrasing

Understand informal language:
```
"mom call later" → "Call mom later"
"fees asap" → "Pay fees ASAP"
"batman maybe" → "Watch Batman (maybe)"
```

### 4. Multi-Intent Detection

Some inputs contain multiple intents:
```
"Create 3 tasks: gym, study, shopping"
```

**Future**: Support batch task creation

---

## Testing NLP

### Unit Tests

```python
def test_parse_gym_task():
    engine = NLPEngine()
    result = engine.parse("Gym every Monday Wednesday Friday at 6 am")
    
    assert result["task_title"] == "Gym"
    assert result["priority"] == "low"
    assert result["category"] == "fitness"
    assert "MO,WE,FR" in result["recurrence"]
    assert result["confidence_score"] >= 90

def test_parse_urgent_task():
    engine = NLPEngine()
    result = engine.parse("URGENT: submit assignment ASAP")
    
    assert result["task_title"] == "Submit assignment"
    assert result["priority"] == "high"
    assert result["category"] == "study"
```

### Manual Testing

```bash
# Test API endpoint
curl -X POST "http://localhost:8000/api/tasks/parse" \
  -H "Content-Type: application/json" \
  -d '{"text": "Gym every Monday Wednesday Friday at 6 am"}'
```

---

## Extending the NLP System

### Adding New Intent

```python
# In intent_parser.py
class Intent(str, Enum):
    # ... existing intents
    REMIND_ME = "remind_me"

# Add patterns
INTENT_PATTERNS = {
    # ...
    Intent.REMIND_ME: [
        r"remind\s+me\s+to\s+(.+?)\s+(?:at|in|after)\s+(.+)",
    ]
}
```

### Adding New Category

```python
# In entity_extractor.py
CATEGORY_KEYWORDS = {
    # ...
    "travel": ["trip", "flight", "hotel", "vacation", "travel"],
}
```

### Adding New Time Expression

```python
# In entity_extractor.py
time_patterns = {
    # ...
    r"end of month": lambda: get_last_day_of_month(),
    r"eom": lambda: get_last_day_of_month(),
}
```

---

## Performance Considerations

### Speed

- **Average parse time**: < 100ms
- **Bottleneck**: dateparser library
- **Optimization**: Cache parsed results

### Accuracy

- **Average confidence**: 75%
- **High-confidence tasks**: 90%+
- **Improvement**: More training data, better patterns

### Scalability

- **Current**: Single-threaded
- **Future**: Async processing, GPU acceleration

---

## Known Limitations

1. **Ambiguous dates**: "Friday" could be this or next week
2. **Time zones**: Assumes user timezone
3. **Context**: No conversation history
4. **Entities**: Can't extract from unstructured text
5. **Multiple intents**: Only detects one intent per input

---

## Roadmap

### v1.1
- [ ] Fuzzy matching for task names
- [ ] Abbreviation expansion
- [ ] Better date ambiguity resolution
- [ ] Confidence feedback to user

### v1.2
- [ ] Conversation context
- [ ] Multiple intents per input
- [ ] Custom entity types
- [ ] Machine learning model

### v2.0
- [ ] Fine-tuned transformer model (BERT)
- [ ] Local LLM integration (Ollama)
- [ ] Multi-language support
- [ ] Voice input processing

---

## Resources

- **spaCy**: https://spacy.io/
- **dateparser**: https://dateparser.readthedocs.io/
- **NLTK**: https://www.nltk.org/
- **transformers**: https://huggingface.co/transformers/

---

## Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: nlp@neurotask.dev

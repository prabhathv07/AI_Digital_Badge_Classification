"""
NLP Phrase Dictionary - Sanitized Excerpt
Author: Prabhath Vinay Vipparthi
Purpose: Student-friendly natural language support for badge level detection
"""

import re
from typing import Dict, Tuple, Optional

# Negation words checked before a matched level phrase
NEGATION_WORDS: frozenset[str] = frozenset([
    "not", "no", "never", "without", "non",
    "doesn't", "don't", "isn't", "aren't", "wasn't", "weren't",
    "cannot", "can't", "couldn't", "won't", "wouldn't",
])


def phrase_matches(phrase: str, text: str) -> Optional[re.Match]:
    """
    Word-boundary-aware matching for level phrases.
    
    Returns the first Match object if `phrase` appears in `text` as a
    whole-word sequence, else None.
    Always case-insensitive.
    """
    pattern = r'\b' + re.escape(phrase) + r'\b'
    return re.search(pattern, text, re.IGNORECASE)


# Student-friendly phrases for Foundational level
FOUNDATIONAL_PHRASES: Dict[str, Tuple[str, str]] = {
    "complete beginners": ("Foundational", "High"),
    "no experience necessary": ("Foundational", "High"),
    "no prior skills": ("Foundational", "High"),
    "from scratch": ("Foundational", "Medium"),
    "zero to hero": ("Foundational", "Medium"),
    "just starting": ("Foundational", "Medium"),
    "beginners welcome": ("Foundational", "Medium"),
    "first time": ("Foundational", "Medium"),
    "step one": ("Foundational", "Medium"),
    "basic concepts": ("Foundational", "Medium"),
    "fundamental skills": ("Foundational", "Medium"),
    "building blocks": ("Foundational", "Medium"),
    "no prerequisites": ("Foundational", "High"),
    "open to beginners": ("Foundational", "Medium"),
    "101": ("Foundational", "Medium"),
    "level one": ("Foundational", "Medium"),
}


# Student-friendly phrases for Milestone level
MILESTONE_PHRASES: Dict[str, Tuple[str, str]] = {
    "builds on": ("Milestone", "High"),
    "building on": ("Milestone", "High"),
    "level up": ("Milestone", "Medium"),
    "moving up": ("Milestone", "Medium"),
    "next step": ("Milestone", "Medium"),
    "step two": ("Milestone", "Medium"),
    "part two": ("Milestone", "Medium"),
    "intermediate level": ("Milestone", "High"),
    "prior experience": ("Milestone", "High"),
    "prior knowledge": ("Milestone", "High"),
    "some experience": ("Milestone", "Medium"),
    "already familiar": ("Milestone", "Medium"),
    "prerequisite course": ("Milestone", "High"),
    "must complete first": ("Milestone", "High"),
    "deepens skills": ("Milestone", "High"),
    "advances skills": ("Milestone", "High"),
    "more advanced": ("Milestone", "Medium"),
    "higher level": ("Milestone", "Medium"),
}


# Student-friendly phrases for Terminal level
TERMINAL_PHRASES: Dict[str, Tuple[str, str]] = {
    "capstone project": ("Terminal", "High"),
    "capstone course": ("Terminal", "High"),
    "capstone badge": ("Terminal", "High"),
    "final step": ("Terminal", "Medium"),
    "final stage": ("Terminal", "Medium"),
    "culminating project": ("Terminal", "High"),
    "culminating experience": ("Terminal", "High"),
    "putting it all together": ("Terminal", "High"),
    "completing the program": ("Terminal", "High"),
    "finishing the series": ("Terminal", "High"),
    "end of the program": ("Terminal", "High"),
    "last course": ("Terminal", "High"),
    "ultimate achievement": ("Terminal", "High"),
    "highest level": ("Terminal", "High"),
}


def extract_level_from_text(text: str) -> Optional[Tuple[str, str]]:
    """
    Extract badge level from description text using student-friendly phrases.
    
    Returns (level, confidence) tuple if a match is found, else None.
    """
    all_phrases = {**FOUNDATIONAL_PHRASES, **MILESTONE_PHRASES, **TERMINAL_PHRASES}
    
    # Sort by length (longest first) for most specific match
    sorted_phrases = sorted(all_phrases.items(), key=lambda x: len(x[0]), reverse=True)
    
    for phrase, (level, confidence) in sorted_phrases:
        if phrase_matches(phrase, text):
            return (level, confidence)
    
    return None


# Example usage
if __name__ == "__main__":
    sample_text = "This workshop is for complete beginners. No experience necessary."
    result = extract_level_from_text(sample_text)
    print(f"Detected level: {result}")  # Output: ('Foundational', 'High')

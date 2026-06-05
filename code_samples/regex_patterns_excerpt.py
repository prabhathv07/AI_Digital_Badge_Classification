"""
Regex Pattern Rules - Sanitized Excerpt
Author: Prabhath Vinay Vipparthi
Purpose: Flexible natural language pattern matching for badge classification
"""

import re
from typing import Tuple, List


class PatternRules:
    """
    Regex patterns for flexible natural language matching.
    Complements the phrase dictionary by catching variations.
    """
    
    # Foundational level patterns
    FOUNDATIONAL_PATTERNS: List[Tuple[re.Pattern, str, str]] = [
        (re.compile(r"just\s+(?:starting|beginning)", re.IGNORECASE), "Foundational", "Medium"),
        (re.compile(r"no\s+(?:experience|background|prior\s+skills)", re.IGNORECASE), "Foundational", "High"),
        (re.compile(r"from\s+(?:scratch|zero)", re.IGNORECASE), "Foundational", "Medium"),
        (re.compile(r"beginner(?:s)?\s+(?:friendly|welcome)", re.IGNORECASE), "Foundational", "Medium"),
        (re.compile(r"first\s+time(?:\s+doing)?", re.IGNORECASE), "Foundational", "Medium"),
    ]
    
    # Milestone level patterns
    MILESTONE_PATTERNS: List[Tuple[re.Pattern, str, str]] = [
        (re.compile(r"(?:builds?|expand(?:s)?)\s+(?:on|upon)", re.IGNORECASE), "Milestone", "High"),
        (re.compile(r"level\s+up", re.IGNORECASE), "Milestone", "Medium"),
        (re.compile(r"next\s+step", re.IGNORECASE), "Milestone", "Medium"),
        (re.compile(r"prior\s+(?:experience|knowledge|background)", re.IGNORECASE), "Milestone", "High"),
        (re.compile(r"(?:already|already\s+have)", re.IGNORECASE), "Milestone", "Medium"),
        (re.compile(r"(?:assumes?|requires?)\s+(?:knowledge|familiarity)", re.IGNORECASE), "Milestone", "High"),
    ]
    
    # Terminal level patterns
    TERMINAL_PATTERNS: List[Tuple[re.Pattern, str, str]] = [
        (re.compile(r"capstone", re.IGNORECASE), "Terminal", "High"),
        (re.compile(r"culminating\s+(?:project|experience|achievement)", re.IGNORECASE), "Terminal", "High"),
        (re.compile(r"putting\s+it\s+all\s+together", re.IGNORECASE), "Terminal", "High"),
        (re.compile(r"(?:completing|finishing)\s+(?:the\s+)?(?:program|series)", re.IGNORECASE), "Terminal", "High"),
        (re.compile(r"final\s+(?:stage|phase|level)", re.IGNORECASE), "Terminal", "Medium"),
    ]
    
    # Assessment type patterns
    ASSESSMENT_PATTERNS: List[Tuple[re.Pattern, str]] = [
        (re.compile(r"just\s+show\s+up", re.IGNORECASE), "attendance"),
        (re.compile(r"physical\s+presence", re.IGNORECASE), "attendance"),
        (re.compile(r"checkpoint\s+quiz", re.IGNORECASE), "knowledge_checks"),
        (re.compile(r"live\s+demo", re.IGNORECASE), "live_demonstration"),
        (re.compile(r"portfolio", re.IGNORECASE), "portfolio"),
        (re.compile(r"practical\s+exam", re.IGNORECASE), "practical_exam"),
    ]
    
    # Real-world context patterns
    REAL_WORLD_PATTERNS: List[re.Pattern] = [
        re.compile(r"client\s+project", re.IGNORECASE),
        re.compile(r"industry\s+partner", re.IGNORECASE),
        re.compile(r"community\s+service", re.IGNORECASE),
        re.compile(r"practicum", re.IGNORECASE),
        re.compile(r"case\s+study", re.IGNORECASE),
        re.compile(r"workplace", re.IGNORECASE),
        re.compile(r"real\s+world", re.IGNORECASE),
    ]
    
    @classmethod
    def extract_level_from_text(cls, text: str) -> Tuple[str, str]:
        """
        Extract badge level using regex patterns.
        Returns (level, confidence) tuple.
        """
        all_patterns = [
            *cls.FOUNDATIONAL_PATTERNS,
            *cls.MILESTONE_PATTERNS,
            *cls.TERMINAL_PATTERNS,
        ]
        
        for pattern, level, confidence in all_patterns:
            if pattern.search(text):
                return (level, confidence)
        
        return ("Foundational", "Low")  # Default fallback
    
    @classmethod
    def extract_assessment_type(cls, text: str) -> str:
        """
        Extract assessment type using regex patterns.
        """
        for pattern, assessment_type in cls.ASSESSMENT_PATTERNS:
            if pattern.search(text):
                return assessment_type
        
        return None
    
    @classmethod
    def has_real_world_context(cls, text: str) -> bool:
        """
        Check if text indicates real-world application.
        """
        for pattern in cls.REAL_WORLD_PATTERNS:
            if pattern.search(text):
                return True
        return False


# Example usage
if __name__ == "__main__":
    # Test level extraction
    text1 = "This workshop is just starting, no experience needed."
    level, confidence = PatternRules.extract_level_from_text(text1)
    print(f"Level: {level}, Confidence: {confidence}")
    
    # Test assessment extraction
    text2 = "Students must just show up to receive the badge."
    assessment = PatternRules.extract_assessment_type(text2)
    print(f"Assessment: {assessment}")
    
    # Test real-world context
    text3 = "Students work on a client project with industry partners."
    has_context = PatternRules.has_real_world_context(text3)
    print(f"Real-world context: {has_context}")

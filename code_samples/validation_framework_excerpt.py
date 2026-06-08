"""
Validation Framework - Sanitized Excerpt
Author: Prabhath Vinay Vipparthi
Purpose: Comprehensive test suite for NLP and classification pipeline
"""

import pytest


class TestNLPStudentLanguage:
    """
    Unit tests for student language phrase extraction.
    Tests that new student-friendly phrases are detected correctly.
    """
    
    def test_foundational_student_phrases_present(self):
        """
        Verify that all Foundational student phrases are in the dictionary.
        """
        from app.services.nlp.phrase_dictionary import LEVEL_PHRASES
        
        expected_phrases = [
            "complete beginners",
            "no experience necessary",
            "from scratch",
            "zero to hero",
            "just starting",
            "beginners welcome",
            "first time",
            "step one",
            "basic concepts",
            "fundamental skills",
        ]
        
        for phrase in expected_phrases:
            assert phrase in LEVEL_PHRASES, f"Phrase '{phrase}' not found in LEVEL_PHRASES"
    
    def test_foundational_phrase_extraction(self):
        """
        Test that Foundational phrases are extracted from badge descriptions.
        """
        from app.services.nlp.phrase_dictionary import LEVEL_PHRASES
        from app.services.nlp.phrase_dictionary import phrase_matches
        
        text = "This workshop is for complete beginners. No experience necessary."
        
        found_phrases = []
        for phrase in LEVEL_PHRASES:
            if phrase_matches(phrase, text):
                found_phrases.append(phrase)
        
        assert "complete beginners" in found_phrases
        assert "no experience necessary" in found_phrases
    
    def test_milestone_student_phrases_present(self):
        """
        Verify that all Milestone student phrases are in the dictionary.
        """
        from app.services.nlp.phrase_dictionary import LEVEL_PHRASES
        
        expected_phrases = [
            "builds on",
            "level up",
            "next step",
            "prior experience",
            "prior knowledge",
            "already familiar",
            "prerequisite course",
            "deepens skills",
            "more advanced",
        ]
        
        for phrase in expected_phrases:
            assert phrase in LEVEL_PHRASES, f"Phrase '{phrase}' not found in LEVEL_PHRASES"
    
    def test_milestone_phrase_extraction(self):
        """
        Test that Milestone phrases are extracted from badge descriptions.
        """
        from app.services.nlp.phrase_dictionary import LEVEL_PHRASES
        from app.services.nlp.phrase_dictionary import phrase_matches
        
        text = "This course builds on prior knowledge. We will level up your skills."
        
        found_phrases = []
        for phrase in LEVEL_PHRASES:
            if phrase_matches(phrase, text):
                found_phrases.append(phrase)
        
        assert "builds on" in found_phrases
        assert "level up" in found_phrases
    
    def test_terminal_student_phrases_present(self):
        """
        Verify that all Terminal student phrases are in the dictionary.
        """
        from app.services.nlp.phrase_dictionary import LEVEL_PHRASES
        
        expected_phrases = [
            "capstone project",
            "capstone course",
            "culminating project",
            "culminating experience",
            "putting it all together",
            "completing the program",
            "finishing the series",
            "ultimate achievement",
        ]
        
        for phrase in expected_phrases:
            assert phrase in LEVEL_PHRASES, f"Phrase '{phrase}' not found in LEVEL_PHRASES"
    
    def test_terminal_phrase_extraction(self):
        """
        Test that Terminal phrases are extracted from badge descriptions.
        """
        from app.services.nlp.phrase_dictionary import LEVEL_PHRASES
        from app.services.nlp.phrase_dictionary import phrase_matches
        
        text = "This capstone project is the culminating experience of the program."
        
        found_phrases = []
        for phrase in LEVEL_PHRASES:
            if phrase_matches(phrase, text):
                found_phrases.append(phrase)
        
        assert "capstone project" in found_phrases
        assert "culminating experience" in found_phrases


class TestEndToEndValidation:
    """
    End-to-end tests that run the full pipeline.
    Tests normalization, NLP extraction, and classification together.
    """
    
    def test_form_foundational_classification(self):
        """
        Test full pipeline on a proposal form with Foundational badge.
        """
        from app.services.normalization.normalizer import normalize
        from app.services.nlp.signal_extractor import extract_all
        from app.services.classification.engine import run_classification
        
        # Load form data
        form_data = {
            "badge_title": "AI for Educators: Foundations",
            "badge_description": "Foundational workshop for faculty",
            "issuer": "LDI",
            "assessment_required": True,
            "assessment_type": "knowledge_checks",
            "assessment_evaluator": "auto_assessed",
            "audience_type": "njit_employee",
        }
        
        # Run full pipeline
        bfs = normalize("form", form_data)
        bfs = extract_all(bfs)
        result = run_classification(bfs)
        
        assert result.level == "Foundational"
        assert result.confidence == "High"
    
    def test_obv3_json_milestone_classification(self):
        """
        Test full pipeline on OBv3 JSON with Milestone badge.
        """
        from app.services.normalization.normalizer import normalize
        from app.services.nlp.signal_extractor import extract_all
        from app.services.classification.engine import run_classification
        
        # Load OBv3 JSON
        obv3_data = {
            "name": "Advanced Python for Data Science",
            "description": "This course builds on prior Python knowledge. Students should already be comfortable with basic programming.",
            "achievementType": "Course",
            "criteria": {
                "narrative": "Complete all modules and submit a portfolio project reviewed by instructors."
            }
        }
        
        # Run full pipeline
        bfs = normalize("obv3_json", obv3_data)
        bfs = extract_all(bfs)
        result = run_classification(bfs)
        
        assert result.level == "Milestone"
        assert "builds on" in bfs.badge_description.lower()
    
    def test_free_text_terminal_classification(self):
        """
        Test full pipeline on free text with Terminal badge.
        """
        from app.services.normalization.normalizer import normalize
        from app.services.nlp.signal_extractor import extract_all
        from app.services.classification.engine import run_classification
        
        # Free text input
        free_text = "This capstone project brings together everything from the data science pathway. Students work on a real client project and present their final design to a panel of instructors. This is the culminating experience of the three-course series."
        
        # Run full pipeline
        bfs = normalize("free_text", free_text)
        bfs = extract_all(bfs)
        result = run_classification(bfs)
        
        assert result.level == "Terminal"
        assert bfs.is_capstone
    
    def test_no_exceptions_thrown(self):
        """
        Verify that all test cases run without exceptions.
        """
        test_cases = [
            ("form", {"badge_title": "Test", "issuer": "LDI"}),
            ("obv3_json", {"name": "Test", "description": "Test"}),
            ("free_text", "This is a test badge description."),
        ]
        
        for input_type, payload in test_cases:
            from app.services.normalization.normalizer import normalize
            bfs = normalize(input_type, payload)
            assert bfs is not None


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])

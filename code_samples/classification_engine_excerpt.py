"""
Classification Engine - Sanitized Excerpt
Author: Prabhath Vinay Vipparthi
Purpose: 3-stage deterministic rule engine for badge classification
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class BadgeFactSheet:
    """
    Normalized internal representation of a badge.
    Contains 60+ fields for classification signals.
    """
    badge_title: str
    badge_description: str
    issuer: str
    assessment_required: bool
    assessment_type: Optional[str]
    assessment_evaluator: Optional[str]
    audience_type: Optional[str]
    self_declared_level: Optional[str]
    canvas_course_code: Optional[str]
    canvas_sequence_number: Optional[int]
    canvas_pathway_length: Optional[int]
    is_capstone: bool
    real_world_context: bool
    badge_purpose: Optional[str]
    # ... additional fields omitted for brevity


@dataclass
class ClassificationResult:
    """Classification output with explanation."""
    category: str
    type: str
    level: str
    confidence: str
    explanation: str
    rules_triggered: list[str]


class ClassificationEngine:
    """
    3-stage deterministic rule engine for badge classification.
    
    Stage 1: Category (Co-Curricular, Academic, Faculty & Staff Development)
    Stage 2: Type (Achievement, Skill, Competency, Souvenir)
    Stage 3: Level (Foundational, Milestone, Terminal, Souvenir)
    """
    
    def __init__(self):
        self.rules_triggered = []
    
    def classify(self, bfs: BadgeFactSheet) -> ClassificationResult:
        """
        Run full 3-stage classification pipeline.
        """
        category = self._classify_category(bfs)
        type_result = self._classify_type(bfs, category)
        level = self._classify_level(bfs, type_result)
        confidence = self._calculate_confidence(bfs, category, type_result, level)
        explanation = self._generate_explanation(bfs, category, type_result, level)
        
        return ClassificationResult(
            category=category,
            type=type_result,
            level=level,
            confidence=confidence,
            explanation=explanation,
            rules_triggered=self.rules_triggered.copy()
        )
    
    def _classify_category(self, bfs: BadgeFactSheet) -> str:
        """
        Stage 1: Determine badge category based on issuer and audience.
        """
        issuer = bfs.issuer.lower()
        audience = bfs.audience_type.lower() if bfs.audience_type else ""
        
        # Rule: OSIL badges are Co-Curricular
        if "osil" in issuer:
            self.rules_triggered.append("S1R01")
            return "Co-Curricular and Extra-Curricular"
        
        # Rule: Makerspace badges are Academic
        if "makerspace" in issuer:
            self.rules_triggered.append("S1R02")
            return "Academic"
        
        # Rule: OGI badges are Academic
        if "ogi" in issuer:
            self.rules_triggered.append("S1R03")
            return "Academic"
        
        # Rule: LDI badges are Faculty & Staff Development
        if "ldi" in issuer:
            self.rules_triggered.append("S1R04")
            return "Faculty and Staff Development"
        
        # Rule: NCE badges are Academic
        if "nce" in issuer:
            self.rules_triggered.append("S1R05")
            return "Academic"
        
        # Default fallback
        return "Academic"
    
    def _classify_type(self, bfs: BadgeFactSheet, category: str) -> str:
        """
        Stage 2: Determine badge type based on assessment and real-world context.
        """
        # Rule: No assessment = Souvenir
        if not bfs.assessment_required:
            self.rules_triggered.append("S2R01")
            return "Souvenir"
        
        # Rule: Expert-scored portfolio = Skill
        if bfs.assessment_evaluator == "expert_scored" and bfs.assessment_type == "portfolio":
            self.rules_triggered.append("S2R02")
            return "Skill"
        
        # Rule: Live demonstration = Skill
        if bfs.assessment_type == "live_demonstration":
            self.rules_triggered.append("S2R03")
            return "Skill"
        
        # Rule: Capstone = Competency
        if bfs.is_capstone:
            self.rules_triggered.append("S2R04")
            return "Competency"
        
        # Rule: Real-world context = Competency
        if bfs.real_world_context:
            self.rules_triggered.append("S2R05")
            return "Competency"
        
        # Default: Achievement
        return "Achievement"
    
    def _classify_level(self, bfs: BadgeFactSheet, type_result: str) -> str:
        """
        Stage 3: Determine badge level based on NLP signals and canvas data.
        """
        # Souvenir badges have Souvenir level
        if type_result == "Souvenir":
            return "Souvenir"
        
        # Rule: Canvas sequence = pathway length = Terminal
        if (bfs.canvas_sequence_number and bfs.canvas_pathway_length and
            bfs.canvas_sequence_number == bfs.canvas_pathway_length):
            self.rules_triggered.append("S3A07")
            return "Terminal"
        
        # Rule: Self-declared level from NLP
        if bfs.self_declared_level:
            return bfs.self_declared_level
        
        # Default fallback
        return "Foundational"
    
    def _calculate_confidence(self, bfs: BadgeFactSheet, category: str, 
                             type_result: str, level: str) -> str:
        """
        Calculate confidence based on signal strength.
        """
        signal_count = sum([
            bfs.assessment_required is not None,
            bfs.assessment_type is not None,
            bfs.assessment_evaluator is not None,
            bfs.audience_type is not None,
            bfs.self_declared_level is not None,
            bfs.canvas_course_code is not None,
        ])
        
        if signal_count >= 5:
            return "High"
        elif signal_count >= 3:
            return "Medium"
        else:
            return "Low"
    
    def _generate_explanation(self, bfs: BadgeFactSheet, category: str, 
                             type_result: str, level: str) -> str:
        """
        Generate human-readable explanation of classification.
        """
        explanation_parts = [
            f"Category: {category}",
            f"Type: {type_result}",
            f"Level: {level}",
        ]
        
        if self.rules_triggered:
            explanation_parts.append(f"Rules: {', '.join(self.rules_triggered)}")
        
        return " | ".join(explanation_parts)


# Example usage
if __name__ == "__main__":
    engine = ClassificationEngine()
    
    bfs = BadgeFactSheet(
        badge_title="AI for Educators",
        badge_description="Foundational workshop for faculty",
        issuer="LDI",
        assessment_required=True,
        assessment_type="knowledge_checks",
        assessment_evaluator="auto_assessed",
        audience_type="njit_employee",
        self_declared_level="Foundational",
        canvas_course_code="MCAI.002.01",
        canvas_sequence_number=1,
        canvas_pathway_length=3,
        is_capstone=False,
        real_world_context=False,
        badge_purpose=None,
    )
    
    result = engine.classify(bfs)
    print(result)

import re
from enum import StrEnum


class QuestionType(StrEnum):
    WHY_COMPANY = "why_company"
    WHY_ROLE = "why_role"
    PROJECT = "project"
    ACHIEVEMENT = "achievement"
    GENERAL = "general"


def classify_question(question: str) -> QuestionType:
    """Classify common application questions without consuming an AI request."""
    text = " ".join(question.casefold().split())

    why_company_phrases = (
        "why do you want to work here",
        "why do you want to work for",
        "why are you interested in our company",
        "why this company",
        "why our company",
        "why us",
        "what interests you about our company",
        "what attracted you to our company",
    )
    why_role_phrases = (
        "why are you interested in this role",
        "why are you interested in this position",
        "why do you want this role",
        "why this role",
        "why this position",
        "what interests you about this role",
        "what interests you about this position",
    )
    project_phrases = (
        "project you are passionate about",
        "project you are proud of",
        "describe a project",
        "tell us about a project",
        "technical challenge",
        "technical problem",
        "most difficult system",
        "challenging project",
    )
    achievement_phrases = (
        "greatest achievement",
        "greatest accomplishment",
        "most significant achievement",
        "most significant accomplishment",
        "something you are proud of",
        "meaningful accomplishment",
        "proudest moment",
    )

    if any(phrase in text for phrase in why_role_phrases):
        return QuestionType.WHY_ROLE
    if any(phrase in text for phrase in why_company_phrases):
        return QuestionType.WHY_COMPANY
    if re.fullmatch(r"why\s+[\w&.' -]+\??", text):
        return QuestionType.WHY_COMPANY
    if any(phrase in text for phrase in project_phrases):
        return QuestionType.PROJECT
    if any(phrase in text for phrase in achievement_phrases):
        return QuestionType.ACHIEVEMENT
    return QuestionType.GENERAL


def should_retrieve_story(question_type: QuestionType) -> bool:
    """Company-specific questions should not reuse an answer about another company."""
    return question_type is not QuestionType.WHY_COMPANY


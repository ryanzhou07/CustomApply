import pytest

from app.classifier import QuestionType, classify_question, should_retrieve_story


@pytest.mark.parametrize(
    ("question", "expected"),
    [
        ("Why Prudential?", QuestionType.WHY_COMPANY),
        ("Why are you interested in this role?", QuestionType.WHY_ROLE),
        ("Tell us about a challenging project.", QuestionType.PROJECT),
        ("What is your greatest achievement?", QuestionType.ACHIEVEMENT),
        ("Tell us something interesting.", QuestionType.GENERAL),
    ],
)
def test_classify_question(question: str, expected: QuestionType) -> None:
    assert classify_question(question) is expected


def test_why_company_does_not_retrieve_an_old_company_story() -> None:
    assert not should_retrieve_story(QuestionType.WHY_COMPANY)

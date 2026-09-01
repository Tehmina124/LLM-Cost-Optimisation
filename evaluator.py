import json
from difflib import SequenceMatcher


def load_questions(file_path="data/test_questions.json"):
    """
    Load evaluation questions from JSON.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def similarity_score(answer, expected_answer):
    """
    Simple text similarity score.

    This is not a perfect LLM evaluation,
    but it provides a reproducible baseline metric.
    """

    answer = answer.lower().strip()
    expected_answer = expected_answer.lower().strip()

    score = SequenceMatcher(
        None,
        answer,
        expected_answer
    ).ratio()

    return round(score * 100, 2)


def evaluate_answer(answer, expected_answer):
    """
    Evaluate one answer.
    """

    score = similarity_score(
        answer,
        expected_answer
    )

    return {
        "quality_score": score,
        "passed": score >= 60
    }


def evaluate_dataset(results):
    """
    Calculate average quality score.
    """

    if not results:
        return 0

    scores = [
        item["quality_score"]
        for item in results
    ]

    return round(
        sum(scores) / len(scores),
        2
    )
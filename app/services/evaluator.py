import re


def _normalize(text):
    return re.sub(r"\s+", " ", str(text or "").strip().lower())


def _keywords(text):
    words = re.findall(r"[a-zA-Z0-9+#.-]{3,}", _normalize(text))

    stop_words = {
        "the", "and", "for", "with", "that", "this",
        "from", "what", "would", "could", "your",
        "have", "about", "into", "when", "where",
        "which", "how", "why"
    }

    return {word for word in words if word not in stop_words}


def score_answer(question, answer):
    """
    Score one interview answer out of 10.

    This rule-based evaluator works without an API key.
    """

    answer = str(answer or "").strip()

    # No answer
    if not answer:
        return 0

    words = answer.split()
    word_count = len(words)

    # Base score according to answer completeness
    if word_count < 5:
        score = 2

    elif word_count < 15:
        score = 4

    elif word_count < 30:
        score = 6

    elif word_count < 60:
        score = 8

    else:
        score = 9

    # Check relevance using important words
    question_words = _keywords(question)
    answer_words = _keywords(answer)

    if question_words:
        overlap = len(question_words & answer_words) / len(question_words)

        if overlap >= 0.60:
            score += 1

        elif overlap < 0.10 and word_count >= 15:
            score -= 1

    return max(0, min(10, score))


def evaluate_answers(questions, answers):

    details = []

    total_score = 0

    for index, question_item in enumerate(questions):

        if isinstance(question_item, dict):

            question = question_item.get(
                "question",
                ""
            )

            difficulty = question_item.get(
                "difficulty",
                "medium"
            )

            question_type = question_item.get(
                "type",
                "Technical"
            )

        else:

            question = str(question_item)

            difficulty = "medium"

            question_type = "Technical"

        answer = (
            answers[index]
            if index < len(answers)
            else ""
        )

        marks = score_answer(
            question,
            answer
        )

        total_score += marks

        details.append({
            "question": question,
            "answer": answer,
            "marks": marks,
            "max_marks": 10,
            "difficulty": difficulty,
            "type": question_type
        })

    max_score = len(questions) * 10

    if max_score > 0:
        percentage = round(
            (total_score / max_score) * 100,
            2
        )
    else:
        percentage = 0

    if percentage >= 80:

        feedback = (
            "Excellent performance. "
            "Your answers show strong understanding."
        )

    elif percentage >= 60:

        feedback = (
            "Good performance. "
            "Review a few concepts and "
            "add more detail to your answers."
        )

    elif percentage >= 40:

        feedback = (
            "Fair performance. "
            "Strengthen your fundamentals "
            "and explain your reasoning more clearly."
        )

    else:

        feedback = (
            "Keep practicing. "
            "Focus on fundamentals and "
            "give more complete answers."
        )

    return {
        "score": total_score,
        "max_score": max_score,
        "percentage": percentage,
        "feedback": feedback,
        "details": details
    }
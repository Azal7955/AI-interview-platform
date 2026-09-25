def evaluate_answers(
    questions,
    answers
):

    if not questions:

        return {
            "score": 0,
            "feedback":
                "No questions available."
        }

    total = 0

    answered = 0

    for answer in answers:

        word_count = len(
            answer.split()
        )

        if word_count >= 35:

            total += 10

            answered += 1

        elif word_count >= 15:

            total += 7

            answered += 1

        elif word_count >= 5:

            total += 4

            answered += 1

    score = round(

        (
            total
            /
            (len(questions) * 10)
        )
        * 100,

        1

    )

    if score >= 80:

        feedback = (
            "Excellent attempt. "
            "Your answers are detailed and structured."
        )

    elif score >= 60:

        feedback = (
            "Good foundation. "
            "Add more technical examples and reasoning."
        )

    elif score >= 40:

        feedback = (
            "Keep practicing. "
            "Try to provide more complete answers."
        )

    else:

        feedback = (
            "More practice is recommended. "
            "Explain your approach and give examples."
        )

    return {

        "score":
            score,

        "answered":
            answered,

        "feedback":
            feedback

    }
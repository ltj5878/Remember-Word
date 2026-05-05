import random


def generate_quiz(all_words: list[dict], num: int, mode: str = "normal") -> list[dict]:
    """
    Generate quiz questions.
    mode: "normal" = show original, pick translation
          "reverse" = show translation, pick original
    """
    questions = random.sample(all_words, min(num, len(all_words)))
    quiz = []
    for q in questions:
        if mode == "normal":
            # Show original, pick correct translation
            correct_answer = q["translation"]
            question_text = q["original"]
            pool_field = "translation"
        else:
            # Show translation, pick correct original
            correct_answer = q["original"]
            question_text = q["translation"]
            pool_field = "original"

        distractor_pool = [w for w in all_words if w[pool_field] != correct_answer]
        distractors = random.sample(distractor_pool, min(3, len(distractor_pool)))
        options = [correct_answer] + [d[pool_field] for d in distractors]
        random.shuffle(options)

        quiz.append({
            "id": q["id"],
            "original": question_text,
            "options": options,
            "answer_index": options.index(correct_answer),
            "mode": mode,
        })
    return quiz

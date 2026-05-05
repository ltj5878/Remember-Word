"""
SM-2 based spaced repetition algorithm (simplified).

Intervals: when correct, interval grows based on ease_factor.
When wrong, reset to 1 day and reduce ease_factor.
"""

from datetime import datetime, timedelta


def calculate_next_review(
    correct: bool,
    review_count: int,
    ease_factor: float,
    interval_days: int,
) -> tuple[int, float, int, datetime]:
    """
    Returns: (new_review_count, new_ease_factor, new_interval_days, next_review_at)
    """
    if correct:
        review_count += 1
        if review_count == 1:
            new_interval = 1
        elif review_count == 2:
            new_interval = 3
        else:
            new_interval = round(interval_days * ease_factor)

        # Slightly increase ease factor on success (cap at 3.0)
        new_ease = min(3.0, ease_factor + 0.1)
    else:
        # Reset on failure
        review_count = 0
        new_interval = 1
        # Decrease ease factor (min 1.3)
        new_ease = max(1.3, ease_factor - 0.2)

    next_review = datetime.now() + timedelta(days=new_interval)
    return review_count, new_ease, new_interval, next_review

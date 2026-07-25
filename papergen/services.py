"""
Core logic for turning a question bank into a randomized paper.

Kept separate from views.py on purpose: this is plain Python + the Django
ORM, no request/response handling. That makes it easy to unit test and easy
to explain in an interview ("business logic lives in a service layer, not
the view").
"""
import random

from questionbank.models import Question


def generate_paper(subject_id, chapter_ids, difficulty_mix, total_marks, seed=None):
    """
    Build a randomized list of questions that:
      - only come from the given chapters
      - roughly follow the requested difficulty proportions
      - sum to (at most) total_marks, without repeating a question

    difficulty_mix example: {"easy": 0.3, "medium": 0.5, "hard": 0.2}
    seed: optional int. Pass the same seed again to reproduce the exact
          same paper later (e.g. for a make-up exam).
    """
    rng = random.Random(seed)

    selected = []
    marks_used = 0
    used_ids = set()

    # Ask for roughly this many marks from each difficulty bucket
    target_marks_per_difficulty = {
        level: round(total_marks * proportion)
        for level, proportion in difficulty_mix.items()
    }

    for level, target_marks in target_marks_per_difficulty.items():
        pool = list(
            Question.objects.filter(
                chapter_id__in=chapter_ids,
                difficulty=level,
            ).exclude(id__in=used_ids)
        )
        rng.shuffle(pool)

        marks_for_this_bucket = 0
        for q in pool:
            if marks_for_this_bucket >= target_marks:
                break
            # Never let a single bucket push the OVERALL paper past the
            # requested total_marks, even if that bucket hasn't hit its
            # own target yet.
            if marks_used + q.marks > total_marks:
                continue
            selected.append(q)
            used_ids.add(q.id)
            marks_for_this_bucket += q.marks
            marks_used += q.marks

    return {
        "questions": selected,
        "total_marks": marks_used,
        "seed": seed if seed is not None else rng.randint(1, 1_000_000),
    }
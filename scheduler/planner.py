from datetime import date
import math


def calculate_priority(difficulty, preparation, exam_date):
    """
    Calculate how urgently a subject should be studied.

    difficulty: 1-10
    preparation: 0-100 percentage
    """

    today = date.today()
    exam = date.fromisoformat(exam_date)

    days_left = (exam - today).days

    # Avoid zero or negative values
    days_left = max(days_left, 1)

    # Higher urgency when exam is closer
    urgency = 60 / days_left

    # Harder subjects get higher priority
    difficulty_score = difficulty * 2

    # Lower preparation means higher priority
    preparation_gap = (100 - preparation) / 10

    priority = (
        urgency
        + difficulty_score
        + preparation_gap
    )

    return round(priority, 2)


def generate_schedule(subjects, study_hours):
    """
    Generate a daily study schedule.
    """

    if not subjects:
        return []

    total_minutes = int(study_hours * 60)

    scored_subjects = []

    for subject in subjects:

        if not subject["exam_date"]:
            continue

        priority = calculate_priority(
            subject["difficulty"],
            subject["preparation"],
            subject["exam_date"]
        )

        scored_subjects.append({
            "name": subject["name"],
            "priority": priority
        })

    if not scored_subjects:
        return []

    # Highest priority first
    scored_subjects.sort(
        key=lambda x: x["priority"],
        reverse=True
    )

    total_priority = sum(
        subject["priority"]
        for subject in scored_subjects
    )

    schedule = []

    for subject in scored_subjects:

        allocated_minutes = (
            subject["priority"] / total_priority
        ) * total_minutes

        # Round to nearest 30 minutes
        allocated_minutes = max(
            30,
            math.floor(allocated_minutes / 30) * 30
        )

        schedule.append({
            "subject": subject["name"],
            "minutes": allocated_minutes,
            "priority": subject["priority"]
        })

    return schedule
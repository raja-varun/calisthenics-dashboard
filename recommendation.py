"""
recommendation.py
Rule-based workout recommendation engine.
"""

import pandas as pd


def get_recommendations(df: pd.DataFrame, user_level: str) -> dict:
    """
    Returns a dict with:
      - routine   : list of recommended exercises
      - message   : motivational text
      - rest_day  : bool
      - focus     : weak muscle group
    """

    if df.empty:
        return _starter_routine(user_level)

    # ── Check last 7 days ──────────────────────────────────────────────────
    recent = df[df["Date"] >= df["Date"].max() - pd.Timedelta(days=6)]
    days_worked = recent["Date"].nunique()

    # Recommend rest if worked out 6+ of last 7 days
    if days_worked >= 6:
        return {
            "routine":  [],
            "message":  "🛌 You've been crushing it! Take a well-earned rest day. Recovery is where gains happen.",
            "rest_day": True,
            "focus":    None,
        }

    # ── Find weak muscle group ────────────────────────────────────────────
    cat_reps = df.groupby("Category")["Reps"].mean()
    weak_cat = cat_reps.idxmin() if not cat_reps.empty else "Upper Body"

    # ── Find lagging exercises ────────────────────────────────────────────
    ex_progress = df.groupby("Exercise_Name")["Reps"].mean()

    # ── Build routine by level ────────────────────────────────────────────
    routines = {
        "Beginner": {
            "Upper Body": ["Incline Pushups", "Knee Pushups", "Dead Hang"],
            "Core":       ["Plank", "Mountain Climbers", "Leg Raises"],
            "Lower Body": ["Squats", "Lunges", "Glute Bridge"],
        },
        "Intermediate": {
            "Upper Body": ["Standard Pushups", "Pullups", "Dips"],
            "Core":       ["Hanging Knee Raises", "Hollow Hold", "Russian Twists"],
            "Lower Body": ["Jump Squats", "Bulgarian Split Squats"],
        },
        "Advanced": {
            "Upper Body":    ["Archer Pushups", "Muscle Ups", "Handstand Pushups"],
            "Core":          ["Dragon Flag", "Toes to Bar", "V-Ups"],
            "Lower Body":    ["Pistol Squats", "Explosive Jump Squats"],
            "Static Skills": ["L-Sit", "Handstand Hold"],
        },
    }

    level_routines = routines.get(user_level, routines["Beginner"])

    # Prioritise the weak category; fill with other categories
    recommended = []
    if weak_cat in level_routines:
        recommended += level_routines[weak_cat][:3]
    for cat, exs in level_routines.items():
        if cat != weak_cat:
            recommended += exs[:2]
    recommended = list(dict.fromkeys(recommended))[:6]  # deduplicate, max 6

    # Special rule: if pullups avg reps < 5, suggest assisted pullups
    pullup_avg = ex_progress.get("Pullups", 999)
    if pullup_avg < 5 and user_level in ("Beginner", "Intermediate"):
        if "Assisted Pullups" not in recommended:
            recommended = ["Assisted Pullups"] + recommended[:5]

    msg_map = {
        "Beginner":     "💪 Keep building those foundations! Consistency beats intensity at this stage.",
        "Intermediate": "🔥 Push harder today — you're in the strength-building phase!",
        "Advanced":     "🚀 Today's session: quality over quantity. Nail those skill movements!",
    }

    return {
        "routine":  recommended,
        "message":  msg_map.get(user_level, "Let's train!"),
        "rest_day": False,
        "focus":    weak_cat,
    }


def _starter_routine(level):
    starters = {
        "Beginner":     ["Incline Pushups", "Squats", "Plank", "Leg Raises", "Lunges"],
        "Intermediate": ["Standard Pushups", "Pullups", "Jump Squats", "Hollow Hold"],
        "Advanced":     ["Muscle Ups", "Handstand Hold", "Dragon Flag", "Pistol Squats"],
    }
    return {
        "routine":  starters.get(level, starters["Beginner"]),
        "message":  "👋 Welcome! Here's your starter routine.",
        "rest_day": False,
        "focus":    "Full Body",
    }

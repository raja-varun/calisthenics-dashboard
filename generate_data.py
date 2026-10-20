"""
generate_data.py
Generates a realistic sample dataset for the Calisthenics Dashboard.
Run this once to create data/workouts.csv
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

random.seed(42)
np.random.seed(42)

# ── Exercise definitions ────────────────────────────────────────────────────
EXERCISES = {
    "Beginner": {
        "Upper Body": ["Incline Pushups", "Knee Pushups", "Negative Pushups", "Assisted Pullups", "Dead Hang"],
        "Core":       ["Plank", "Mountain Climbers", "Leg Raises"],
        "Lower Body": ["Squats", "Lunges", "Glute Bridge", "Calf Raises"],
    },
    "Intermediate": {
        "Upper Body": ["Standard Pushups", "Diamond Pushups", "Pullups", "Chinups", "Dips", "Pike Pushups"],
        "Core":       ["Hanging Knee Raises", "Russian Twists", "Hollow Hold"],
        "Lower Body": ["Jump Squats", "Bulgarian Split Squats", "Pistol Squat Progressions"],
    },
    "Advanced": {
        "Upper Body":    ["Archer Pushups", "One Arm Pushup Progression", "Muscle Ups",
                          "Handstand Pushups", "Front Lever Progression", "Back Lever Progression"],
        "Core":          ["Dragon Flag", "Toes to Bar", "V-Ups"],
        "Lower Body":    ["Pistol Squats", "Explosive Jump Squats", "Nordic Curls"],
        "Static Skills": ["L-Sit", "Handstand Hold", "Planche Progression"],
    },
}

CALORIE_MAP = {
    "Incline Pushups": 4, "Knee Pushups": 4, "Negative Pushups": 5, "Assisted Pullups": 6,
    "Dead Hang": 3, "Plank": 4, "Mountain Climbers": 8, "Leg Raises": 5,
    "Squats": 6, "Lunges": 7, "Glute Bridge": 5, "Calf Raises": 4,
    "Standard Pushups": 7, "Diamond Pushups": 7, "Pullups": 10, "Chinups": 9,
    "Dips": 8, "Pike Pushups": 7, "Hanging Knee Raises": 7, "Russian Twists": 6,
    "Hollow Hold": 5, "Jump Squats": 10, "Bulgarian Split Squats": 9,
    "Pistol Squat Progressions": 9, "Archer Pushups": 9,
    "One Arm Pushup Progression": 10, "Muscle Ups": 14, "Handstand Pushups": 12,
    "Front Lever Progression": 11, "Back Lever Progression": 11,
    "Dragon Flag": 10, "Toes to Bar": 9, "V-Ups": 8,
    "Pistol Squats": 10, "Explosive Jump Squats": 12, "Nordic Curls": 10,
    "L-Sit": 7, "Handstand Hold": 8, "Planche Progression": 12,
}

USER_PROFILES = [
    {"name": "Arjun",  "level": "Beginner",     "weight_start": 72, "height": 1.74, "age": 21, "consistency": 0.75},
    {"name": "Priya",  "level": "Beginner",     "weight_start": 58, "height": 1.62, "age": 20, "consistency": 0.65},
    {"name": "Rahul",  "level": "Intermediate", "weight_start": 78, "height": 1.80, "age": 24, "consistency": 0.85},
    {"name": "Sneha",  "level": "Intermediate", "weight_start": 63, "height": 1.65, "age": 22, "consistency": 0.80},
    {"name": "Vikram", "level": "Advanced",     "weight_start": 75, "height": 1.78, "age": 27, "consistency": 0.92},
    {"name": "Kavya",  "level": "Advanced",     "weight_start": 60, "height": 1.68, "age": 25, "consistency": 0.90},
]

def generate_rows():
    rows = []
    end_date   = datetime.today()
    start_date = end_date - timedelta(days=180)

    for user in USER_PROFILES:
        level     = user["level"]
        ex_map    = EXERCISES[level]
        date      = start_date
        weight    = user["weight_start"]
        streak    = 0
        day_idx   = 0

        while date <= end_date:
            worked_out = random.random() < user["consistency"]
            if worked_out:
                # pick 2-4 exercises across categories
                all_ex = [ex for exs in ex_map.values() for ex in exs]
                chosen = random.sample(all_ex, k=min(random.randint(2, 4), len(all_ex)))
                streak += 1

                # weight drifts slightly over time
                weight = round(user["weight_start"] - (day_idx * 0.01) + random.uniform(-0.3, 0.3), 1)
                bmi    = round(weight / (user["height"] ** 2), 1)

                # skill level grows
                skill_pct = min(100, int(10 + day_idx * 0.3 + random.uniform(-5, 5)))

                # reps improve over time
                rep_mult = 1 + day_idx * 0.002

                for cat, exs in ex_map.items():
                    for ex in exs:
                        if ex not in chosen:
                            continue
                        base_reps = {"Beginner": 8, "Intermediate": 12, "Advanced": 8}[level]
                        reps      = max(1, int(base_reps * rep_mult + random.randint(-2, 4)))
                        sets      = random.randint(2, 4)
                        duration  = round(random.uniform(20, 60), 1)
                        cal_base  = CALORIE_MAP.get(ex, 6)
                        calories  = round(cal_base * sets * reps * random.uniform(0.08, 0.12), 1)

                        rows.append({
                            "Date":             date.strftime("%Y-%m-%d"),
                            "User":             user["name"],
                            "User_Level":       level,
                            "Exercise_Name":    ex,
                            "Category":         cat,
                            "Sets":             sets,
                            "Reps":             reps,
                            "Calories_Burned":  calories,
                            "Workout_Duration": duration,
                            "Weight":           weight,
                            "Height":           user["height"],
                            "BMI":              bmi,
                            "Skill_Level":      skill_pct,
                            "Workout_Completed": 1,
                            "Streak":           streak,
                        })
            else:
                streak = 0

            date    += timedelta(days=1)
            day_idx += 1

    return pd.DataFrame(rows)


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    df = generate_rows()
    df.to_csv("data/workouts.csv", index=False)
    print(f"✅  Generated {len(df)} rows → data/workouts.csv")

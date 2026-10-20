"""
analytics.py
Helper functions for data processing and chart generation.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Colour palette ──────────────────────────────────────────────────────────
C_PRIMARY   = "#00F5A0"   # neon green
C_ACCENT    = "#00D9F5"   # cyan
C_WARN      = "#FFB347"   # orange
C_DANGER    = "#FF6B6B"   # red
C_BG        = "#0D0D0D"
C_CARD      = "#1A1A2E"
C_TEXT      = "#E0E0E0"

PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=C_TEXT, family="Rajdhani, sans-serif"),
    margin=dict(l=20, r=20, t=40, b=20),
)


# ── Data loaders ────────────────────────────────────────────────────────────
def load_data(path="data/workouts.csv") -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["Date"])
    return df


def filter_user(df: pd.DataFrame, user: str) -> pd.DataFrame:
    if user == "All":
        return df
    return df[df["User"] == user]


# ── KPI helpers ─────────────────────────────────────────────────────────────
def total_workouts(df):
    return int(df["Workout_Completed"].sum())


def total_calories(df):
    return round(df["Calories_Burned"].sum(), 1)


def total_hours(df):
    return round(df["Workout_Duration"].sum() / 60, 1)


def current_streak(df):
    if df.empty:
        return 0
    return int(df["Streak"].max())


def weekly_consistency(df):
    """% of days in the last 7 days that had a workout."""
    last7 = df[df["Date"] >= df["Date"].max() - pd.Timedelta(days=6)]
    unique_days = last7["Date"].nunique()
    return round(unique_days / 7 * 100, 1)


# ── Progress charts ─────────────────────────────────────────────────────────
def exercise_progress_chart(df, exercise_name):
    sub = df[df["Exercise_Name"] == exercise_name].groupby("Date")["Reps"].mean().reset_index()
    fig = px.line(sub, x="Date", y="Reps",
                  title=f"{exercise_name} — Reps Over Time",
                  color_discrete_sequence=[C_PRIMARY])
    fig.update_traces(line_width=2.5, mode="lines+markers",
                      marker=dict(size=5, color=C_ACCENT))
    fig.update_layout(**PLOT_LAYOUT)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.05)")
    return fig


def calories_trend_chart(df):
    sub = df.groupby("Date")["Calories_Burned"].sum().reset_index()
    fig = px.area(sub, x="Date", y="Calories_Burned",
                  title="Daily Calories Burned",
                  color_discrete_sequence=[C_PRIMARY])
    fig.update_traces(line_color=C_PRIMARY, fillcolor=f"rgba(0,245,160,0.15)")
    fig.update_layout(**PLOT_LAYOUT)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.05)")
    return fig


def duration_trend_chart(df):
    sub = df.groupby("Date")["Workout_Duration"].mean().reset_index()
    fig = px.bar(sub, x="Date", y="Workout_Duration",
                 title="Average Workout Duration (min)",
                 color_discrete_sequence=[C_ACCENT])
    fig.update_layout(**PLOT_LAYOUT)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.05)")
    return fig


def muscle_group_bar(df):
    sub = df.groupby("Category")["Calories_Burned"].sum().reset_index()
    fig = px.bar(sub, x="Category", y="Calories_Burned",
                 title="Calories by Muscle Group",
                 color="Calories_Burned",
                 color_continuous_scale=["#00D9F5", "#00F5A0"])
    fig.update_layout(**PLOT_LAYOUT, coloraxis_showscale=False)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.05)")
    return fig


# ── Consistency ─────────────────────────────────────────────────────────────
def heatmap_chart(df):
    df2 = df.copy()
    df2["Week"]    = df2["Date"].dt.isocalendar().week.astype(int)
    df2["Weekday"] = df2["Date"].dt.day_name()
    pivot = df2.groupby(["Week", "Weekday"])["Workout_Completed"].sum().reset_index()
    pivot = pivot.pivot(index="Weekday", columns="Week", values="Workout_Completed").fillna(0)
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    pivot = pivot.reindex([d for d in day_order if d in pivot.index])

    fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=[f"W{c}" for c in pivot.columns],
        y=pivot.index.tolist(),
        colorscale=[[0, "#1A1A2E"], [0.5, "#005F5F"], [1, "#00F5A0"]],
        showscale=False,
    ))
    fig.update_layout(title="Workout Heatmap", **PLOT_LAYOUT)
    return fig


def weekly_activity_chart(df):
    df2 = df.copy()
    df2["Week"] = df2["Date"].dt.to_period("W").astype(str)
    sub = df2.groupby("Week")["Workout_Completed"].sum().reset_index()
    fig = px.bar(sub, x="Week", y="Workout_Completed",
                 title="Weekly Workout Count",
                 color_discrete_sequence=[C_PRIMARY])
    fig.update_layout(**PLOT_LAYOUT)
    fig.update_xaxes(showgrid=False, tickangle=45)
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.05)")
    return fig


def best_day(df):
    if df.empty:
        return "N/A"
    return df.groupby(df["Date"].dt.day_name())["Workout_Completed"].sum().idxmax()


def most_skipped_day(df):
    if df.empty:
        return "N/A"
    return df.groupby(df["Date"].dt.day_name())["Workout_Completed"].sum().idxmin()


# ── BMI ─────────────────────────────────────────────────────────────────────
def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight", C_ACCENT
    elif bmi < 25:
        return "Normal ✅", C_PRIMARY
    elif bmi < 30:
        return "Overweight", C_WARN
    else:
        return "Obese", C_DANGER


def weight_trend_chart(df):
    sub = df.dropna(subset=["Weight"]).groupby("Date")["Weight"].mean().reset_index()
    fig = px.line(sub, x="Date", y="Weight",
                  title="Weight Trend (kg)",
                  color_discrete_sequence=[C_WARN])
    fig.update_traces(line_width=2.5, mode="lines+markers",
                      marker=dict(size=5, color=C_WARN))
    fig.update_layout(**PLOT_LAYOUT)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.05)")
    return fig


# ── Skills ──────────────────────────────────────────────────────────────────
SKILLS = ["Muscle Ups", "Handstand Hold", "L-Sit", "Front Lever Progression", "Planche Progression"]


def skill_radar_chart(df):
    skill_scores = []
    for skill in SKILLS:
        sub = df[df["Exercise_Name"] == skill]
        score = int(sub["Skill_Level"].mean()) if not sub.empty else random.randint(10, 40)
        skill_scores.append(score)

    fig = go.Figure(go.Scatterpolar(
        r=skill_scores + [skill_scores[0]],
        theta=SKILLS + [SKILLS[0]],
        fill="toself",
        fillcolor=f"rgba(0,245,160,0.15)",
        line=dict(color=C_PRIMARY, width=2),
        marker=dict(color=C_ACCENT, size=6),
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100],
                            gridcolor="rgba(255,255,255,0.1)",
                            tickfont=dict(color=C_TEXT)),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.1)",
                             tickfont=dict(color=C_TEXT)),
        ),
        showlegend=False,
        title="Skill Radar",
        **PLOT_LAYOUT,
    )
    return fig


# ── Calories analytics ──────────────────────────────────────────────────────
def calories_pie(df):
    sub = df.groupby("Category")["Calories_Burned"].sum().reset_index()
    fig = px.pie(sub, values="Calories_Burned", names="Category",
                 title="Calorie Distribution by Category",
                 color_discrete_sequence=[C_PRIMARY, C_ACCENT, C_WARN, C_DANGER, "#A78BFA"])
    fig.update_traces(textposition="inside", textinfo="percent+label",
                      hole=0.4, marker=dict(line=dict(color=C_BG, width=2)))
    fig.update_layout(**PLOT_LAYOUT)
    return fig


def monthly_calories_bar(df):
    df2 = df.copy()
    df2["Month"] = df2["Date"].dt.to_period("M").astype(str)
    sub = df2.groupby("Month")["Calories_Burned"].sum().reset_index()
    fig = px.bar(sub, x="Month", y="Calories_Burned",
                 title="Monthly Calories Burned",
                 color_discrete_sequence=[C_ACCENT])
    fig.update_layout(**PLOT_LAYOUT)
    fig.update_xaxes(showgrid=False, tickangle=45)
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.05)")
    return fig


# ── Exercise Library ────────────────────────────────────────────────────────
import random  # needed above too

EXERCISE_LIBRARY = {
    "Incline Pushups":          {"level": "Beginner",     "muscle": "Chest, Triceps", "reps": "3×10",  "tip": "Keep body straight; use a wall or bench."},
    "Knee Pushups":             {"level": "Beginner",     "muscle": "Chest, Triceps", "reps": "3×12",  "tip": "Great for building chest foundation."},
    "Negative Pushups":         {"level": "Beginner",     "muscle": "Chest, Triceps", "reps": "3×5",   "tip": "Lower slowly for 4 seconds."},
    "Assisted Pullups":         {"level": "Beginner",     "muscle": "Back, Biceps",   "reps": "3×6",   "tip": "Use a band or have a partner assist."},
    "Dead Hang":                {"level": "Beginner",     "muscle": "Grip, Lats",     "reps": "3×30s", "tip": "Hang fully relaxed; builds grip strength."},
    "Plank":                    {"level": "Beginner",     "muscle": "Core",           "reps": "3×30s", "tip": "Keep hips level; breathe normally."},
    "Mountain Climbers":        {"level": "Beginner",     "muscle": "Core, Cardio",   "reps": "3×20",  "tip": "Drive knees fast for cardio benefit."},
    "Leg Raises":               {"level": "Beginner",     "muscle": "Lower Abs",      "reps": "3×12",  "tip": "Keep lower back pressed to floor."},
    "Squats":                   {"level": "Beginner",     "muscle": "Quads, Glutes",  "reps": "3×15",  "tip": "Go below parallel if possible."},
    "Lunges":                   {"level": "Beginner",     "muscle": "Quads, Glutes",  "reps": "3×12",  "tip": "Keep torso upright."},
    "Glute Bridge":             {"level": "Beginner",     "muscle": "Glutes, Hams",   "reps": "3×15",  "tip": "Squeeze glutes at the top."},
    "Calf Raises":              {"level": "Beginner",     "muscle": "Calves",         "reps": "3×20",  "tip": "Do single-leg for more challenge."},
    "Standard Pushups":         {"level": "Intermediate", "muscle": "Chest, Triceps", "reps": "4×15",  "tip": "Full range of motion is key."},
    "Diamond Pushups":          {"level": "Intermediate", "muscle": "Triceps, Chest", "reps": "3×10",  "tip": "Hands form a diamond shape."},
    "Pullups":                  {"level": "Intermediate", "muscle": "Back, Biceps",   "reps": "4×8",   "tip": "Pull elbows down, not arms."},
    "Chinups":                  {"level": "Intermediate", "muscle": "Biceps, Back",   "reps": "4×8",   "tip": "Supinated grip; great for biceps."},
    "Dips":                     {"level": "Intermediate", "muscle": "Chest, Triceps", "reps": "3×10",  "tip": "Lean forward for chest focus."},
    "Pike Pushups":             {"level": "Intermediate", "muscle": "Shoulders",      "reps": "3×10",  "tip": "Hips high; targets deltoids."},
    "Hanging Knee Raises":      {"level": "Intermediate", "muscle": "Abs, Hip Flex",  "reps": "3×12",  "tip": "Control the descent."},
    "Russian Twists":           {"level": "Intermediate", "muscle": "Obliques",       "reps": "3×20",  "tip": "Lift feet for added difficulty."},
    "Hollow Hold":              {"level": "Intermediate", "muscle": "Full Core",      "reps": "3×30s", "tip": "Press lower back into floor."},
    "Jump Squats":              {"level": "Intermediate", "muscle": "Quads, Calves",  "reps": "3×12",  "tip": "Land softly; knees over toes."},
    "Bulgarian Split Squats":   {"level": "Intermediate", "muscle": "Quads, Glutes",  "reps": "3×10",  "tip": "Rear foot elevated on bench."},
    "Pistol Squat Progressions":{"level": "Intermediate", "muscle": "Quads, Balance", "reps": "3×6",   "tip": "Use support initially."},
    "Archer Pushups":           {"level": "Advanced",     "muscle": "Chest, Triceps", "reps": "4×6",   "tip": "Shift weight side to side."},
    "One Arm Pushup Progression":{"level": "Advanced",   "muscle": "Full Upper Body", "reps": "3×5",   "tip": "Start with feet wide."},
    "Muscle Ups":               {"level": "Advanced",     "muscle": "Back, Chest",    "reps": "3×5",   "tip": "Explosive pull, then push above bar."},
    "Handstand Pushups":        {"level": "Advanced",     "muscle": "Shoulders",      "reps": "3×5",   "tip": "Practice kick-up against wall first."},
    "Front Lever Progression":  {"level": "Advanced",     "muscle": "Lats, Core",     "reps": "3×10s", "tip": "Progress: tuck → straddle → full."},
    "Back Lever Progression":   {"level": "Advanced",     "muscle": "Shoulders, Core","reps": "3×10s", "tip": "Start with tuck position."},
    "Dragon Flag":              {"level": "Advanced",     "muscle": "Full Core",      "reps": "3×6",   "tip": "Grip a bench; lower body straight."},
    "Toes to Bar":              {"level": "Advanced",     "muscle": "Abs, Hip Flex",  "reps": "3×8",   "tip": "Use hip drive for momentum."},
    "V-Ups":                    {"level": "Advanced",     "muscle": "Full Abs",       "reps": "3×12",  "tip": "Touch feet and hands at top."},
    "Pistol Squats":            {"level": "Advanced",     "muscle": "Quads, Balance", "reps": "3×6",   "tip": "Extend arms for counterbalance."},
    "Explosive Jump Squats":    {"level": "Advanced",     "muscle": "Legs, Power",    "reps": "3×10",  "tip": "Max height every rep."},
    "Nordic Curls":             {"level": "Advanced",     "muscle": "Hamstrings",     "reps": "3×5",   "tip": "Anchor feet; lower slowly."},
    "L-Sit":                    {"level": "Advanced",     "muscle": "Abs, Triceps",   "reps": "3×15s", "tip": "Keep legs perfectly straight."},
    "Handstand Hold":           {"level": "Advanced",     "muscle": "Shoulders, Core","reps": "3×15s", "tip": "Wall-assisted first; find balance."},
    "Planche Progression":      {"level": "Advanced",     "muscle": "Full Upper Body", "reps": "3×10s", "tip": "Lean forward on tuck planche."},
}

"""
app.py  —  Calisthenics Progress Dashboard
Run with:  streamlit run app.py
"""

import os, datetime, random
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from analytics       import (load_data, filter_user, total_workouts, total_calories,
                              total_hours, current_streak, weekly_consistency,
                              exercise_progress_chart, calories_trend_chart,
                              duration_trend_chart, muscle_group_bar,
                              heatmap_chart, weekly_activity_chart,
                              best_day, most_skipped_day, bmi_category,
                              weight_trend_chart, skill_radar_chart,
                              calories_pie, monthly_calories_bar,
                              EXERCISE_LIBRARY, SKILLS, PLOT_LAYOUT,
                              C_PRIMARY, C_ACCENT, C_WARN, C_DANGER, C_BG, C_TEXT)
from recommendation  import get_recommendations

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title  = "CaliFit Dashboard",
    page_icon   = "🏋️",
    layout      = "wide",
    initial_sidebar_state = "expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Orbitron:wght@700;900&family=Inter:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    background-color: #0D0D0D;
    color: #E0E0E0;
    font-family: 'Rajdhani', sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1117 0%, #0D0D1F 100%);
    border-right: 1px solid rgba(0,245,160,0.15);
}
[data-testid="stSidebar"] * { color: #E0E0E0 !important; }

/* KPI Cards */
.kpi-card {
    background: linear-gradient(135deg, #12122A 0%, #0D1A1A 100%);
    border: 1px solid rgba(0,245,160,0.2);
    border-radius: 12px;
    padding: 18px 22px;
    text-align: center;
    transition: border-color 0.3s;
}
.kpi-card:hover { border-color: rgba(0,245,160,0.6); }
.kpi-value {
    font-family: 'Orbitron', monospace;
    font-size: 2rem;
    font-weight: 900;
    color: #00F5A0;
    display: block;
    line-height: 1.1;
}
.kpi-label {
    font-size: 0.8rem;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 6px;
    display: block;
}
.kpi-icon { font-size: 1.6rem; margin-bottom: 6px; display: block; }

/* Section headers */
.section-title {
    font-family: 'Orbitron', monospace;
    font-size: 1.3rem;
    color: #00F5A0;
    border-left: 3px solid #00F5A0;
    padding-left: 12px;
    margin: 24px 0 16px 0;
    text-transform: uppercase;
    letter-spacing: 2px;
}

/* Exercise badge */
.ex-badge {
    display: inline-block;
    background: rgba(0,245,160,0.1);
    border: 1px solid rgba(0,245,160,0.3);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.85rem;
    margin: 3px;
    color: #00F5A0;
}
.ex-badge.inter { background: rgba(0,217,245,0.1); border-color: rgba(0,217,245,0.3); color: #00D9F5; }
.ex-badge.adv   { background: rgba(255,107,107,0.1); border-color: rgba(255,107,107,0.3); color: #FF6B6B; }

/* Progress bar */
.prog-wrap { margin: 10px 0; }
.prog-label { font-size: 0.85rem; color: #aaa; margin-bottom: 4px; }
.prog-bar-bg { background: #1A1A2E; border-radius: 20px; height: 10px; overflow: hidden; }
.prog-bar-fill { height: 10px; border-radius: 20px;
                  background: linear-gradient(90deg, #00D9F5, #00F5A0); }

/* Library card */
.lib-card {
    background: #12122A;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 10px;
    transition: border-color 0.2s;
}
.lib-card:hover { border-color: rgba(0,245,160,0.4); }
.lib-title { font-size: 1.05rem; font-weight: 600; color: #00F5A0; margin-bottom: 6px; }
.lib-meta  { font-size: 0.8rem; color: #888; }

/* Recommendation card */
.rec-card {
    background: linear-gradient(135deg, #0D1A1A, #0A1020);
    border: 1px solid rgba(0,245,160,0.3);
    border-radius: 14px;
    padding: 22px;
    margin-bottom: 14px;
}

/* Streamlit overrides */
div[data-testid="stMetricValue"] { color: #00F5A0 !important; font-family: 'Orbitron', monospace !important; }
.stSelectbox label, .stDateInput label, .stNumberInput label { color: #aaa !important; font-size: 0.85rem !important; }
.stButton > button {
    background: linear-gradient(90deg, #00D9F5, #00F5A0);
    color: #0D0D0D;
    font-family: 'Orbitron', monospace;
    font-weight: 700;
    border: none;
    border-radius: 8px;
    padding: 10px 28px;
    letter-spacing: 1px;
    transition: opacity 0.2s;
}
.stButton > button:hover { opacity: 0.85; }
hr { border-color: rgba(255,255,255,0.07) !important; }
</style>
""", unsafe_allow_html=True)


# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    if os.path.exists("data/workouts.csv"):
        return load_data("data/workouts.csv")
    st.error("data/workouts.csv not found. Run `python generate_data.py` first.")
    return pd.DataFrame()

df_all = get_data()


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 16px 0 24px 0;'>
        <div style='font-family:Orbitron,monospace; font-size:1.4rem; color:#00F5A0; font-weight:900;'>⚡ CALIFIT</div>
        <div style='font-size:0.72rem; color:#555; letter-spacing:3px; text-transform:uppercase;'>Progress Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    pages = {
        "🏠  Home Dashboard":       "home",
        "📋  Workout Tracker":      "tracker",
        "📈  Progress Analytics":   "progress",
        "🔥  Consistency Analysis": "consistency",
        "⚖️  BMI & Body Metrics":   "bmi",
        "🎯  Skill Progression":    "skills",
        "🤖  Recommendations":      "reco",
        "🔥  Calorie Analytics":    "calories",
        "📚  Exercise Library":     "library",
    }
    page_label = st.radio("Navigate", list(pages.keys()), label_visibility="collapsed")
    page = pages[page_label]

    st.markdown("---")
    users = ["All"] + sorted(df_all["User"].unique().tolist()) if not df_all.empty else ["All"]
    sel_user = st.selectbox("👤 Filter by User", users)
    sel_level = st.selectbox("🏅 Level", ["All", "Beginner", "Intermediate", "Advanced"])

    df = filter_user(df_all, sel_user)
    if sel_level != "All" and not df.empty:
        df = df[df["User_Level"] == sel_level]

    st.markdown("---")
    st.markdown("<div style='font-size:0.7rem; color:#444; text-align:center;'>DVT Project · B.Tech 2025</div>",
                unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def kpi(icon, value, label):
    return f"""<div class="kpi-card">
        <span class="kpi-icon">{icon}</span>
        <span class="kpi-value">{value}</span>
        <span class="kpi-label">{label}</span>
    </div>"""

def section(title):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)

def progress_bar(label, pct, color="#00F5A0"):
    st.markdown(f"""<div class="prog-wrap">
        <div class="prog-label">{label} — {pct}%</div>
        <div class="prog-bar-bg"><div class="prog-bar-fill" style="width:{pct}%; background: linear-gradient(90deg, #00D9F5, {color});"></div></div>
    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 1 — HOME DASHBOARD
# ════════════════════════════════════════════════════════════════════════════
if page == "home":
    st.markdown("""
    <div style='padding: 10px 0 24px 0;'>
        <div style='font-family:Orbitron,monospace; font-size:2rem; font-weight:900; color:#00F5A0;'>
            CALISTHENICS DASHBOARD
        </div>
        <div style='color:#666; letter-spacing:3px; font-size:0.8rem; text-transform:uppercase;'>
            FITNESS ANALYTICS SYSTEM
        </div>
    </div>
    """, unsafe_allow_html=True)

    if df.empty:
        st.warning("No data found. Log some workouts first!")
    else:
        tw = total_workouts(df)
        tc = total_calories(df)
        th = total_hours(df)
        cs = current_streak(df)
        wc = weekly_consistency(df)
        bmi_val = round(df["BMI"].mean(), 1) if "BMI" in df else 0.0

        c1, c2, c3, c4, c5, c6 = st.columns(6)
        for col, icon, val, lbl in zip(
            [c1, c2, c3, c4, c5, c6],
            ["🏋️", "🔥", "⏱️", "⚡", "📊", "⚖️"],
            [tw, f"{tc:,.0f}", th, cs, f"{wc}%", bmi_val],
            ["Workouts", "Calories", "Hours", "Best Streak", "Weekly %", "Avg BMI"],
        ):
            col.markdown(kpi(icon, val, lbl), unsafe_allow_html=True)

        st.markdown("")
        section("RECENT ACTIVITY")

        col_a, col_b = st.columns(2)
        with col_a:
            st.plotly_chart(calories_trend_chart(df), use_container_width=True)
        with col_b:
            st.plotly_chart(muscle_group_bar(df), use_container_width=True)

        section("CONSISTENCY OVERVIEW")
        progress_bar("Weekly Consistency", min(int(wc), 100))
        progress_bar("Monthly Completion", min(random.randint(60, 95), 100), color="#FF6B6B")
        progress_bar("Streak Score",       min(cs * 5, 100), color="#FFB347")


# ════════════════════════════════════════════════════════════════════════════
# PAGE 2 — WORKOUT TRACKER
# ════════════════════════════════════════════════════════════════════════════
elif page == "tracker":
    section("LOG YOUR WORKOUT")

    EXERCISES_MAP = {
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
            "Upper Body":    ["Archer Pushups", "One Arm Pushup Progression", "Muscle Ups", "Handstand Pushups", "Front Lever Progression", "Back Lever Progression"],
            "Core":          ["Dragon Flag", "Toes to Bar", "V-Ups"],
            "Lower Body":    ["Pistol Squats", "Explosive Jump Squats", "Nordic Curls"],
            "Static Skills": ["L-Sit", "Handstand Hold", "Planche Progression"],
        },
    }

    with st.form("workout_form"):
        c1, c2 = st.columns(2)
        with c1:
            log_date  = st.date_input("📅 Date", value=datetime.date.today())
            log_user  = st.text_input("👤 Your Name", value="User1")
            log_level = st.selectbox("🏅 Level", ["Beginner", "Intermediate", "Advanced"])
        with c2:
            log_cat = st.selectbox("💪 Category", list(EXERCISES_MAP["Beginner"].keys()))
            all_ex  = [e for cat in EXERCISES_MAP[log_level].values() for e in cat]
            log_ex  = st.selectbox("🏋️ Exercise", all_ex)
            log_sets = st.number_input("Sets",      min_value=1, max_value=10, value=3)

        c3, c4, c5 = st.columns(3)
        with c3: log_reps = st.number_input("Reps",     min_value=1,  max_value=200, value=10)
        with c4: log_dur  = st.number_input("Duration (min)", min_value=1, max_value=180, value=30)
        with c5: log_cal  = st.number_input("Calories Burned", min_value=1, max_value=2000, value=80)

        submitted = st.form_submit_button("💾  LOG WORKOUT")

        if submitted:
            weight_est = 70.0
            new_row = {
                "Date": str(log_date), "User": log_user, "User_Level": log_level,
                "Exercise_Name": log_ex, "Category": log_cat,
                "Sets": log_sets, "Reps": log_reps,
                "Calories_Burned": log_cal, "Workout_Duration": log_dur,
                "Weight": weight_est, "Height": 1.75,
                "BMI": round(weight_est / 1.75**2, 1),
                "Skill_Level": 50, "Workout_Completed": 1, "Streak": 1,
            }
            new_df = pd.DataFrame([new_row])
            os.makedirs("data", exist_ok=True)
            header = not os.path.exists("data/workouts.csv")
            new_df.to_csv("data/workouts.csv", mode="a", header=header, index=False)
            st.success(f"✅ Workout logged! {log_sets}×{log_reps} {log_ex} saved.")
            st.cache_data.clear()

    section("RECENT WORKOUT LOG")
    if not df.empty:
        show_cols = ["Date", "User", "Exercise_Name", "Category", "Sets", "Reps", "Calories_Burned", "Workout_Duration"]
        recent = df.sort_values("Date", ascending=False).head(20)[show_cols]
        st.dataframe(recent, use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 3 — PROGRESS ANALYTICS
# ════════════════════════════════════════════════════════════════════════════
elif page == "progress":
    section("STRENGTH PROGRESS")

    avail_ex = df["Exercise_Name"].unique().tolist() if not df.empty else ["Pullups"]
    sel_ex = st.selectbox("Select Exercise", sorted(avail_ex))

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(exercise_progress_chart(df, sel_ex), use_container_width=True)
    with c2:
        st.plotly_chart(calories_trend_chart(df), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(duration_trend_chart(df), use_container_width=True)
    with c4:
        st.plotly_chart(muscle_group_bar(df), use_container_width=True)

    section("EXERCISE VOLUME BREAKDOWN")
    if not df.empty:
        top_ex = df.groupby("Exercise_Name")["Reps"].sum().nlargest(10).reset_index()
        fig = px.bar(top_ex, x="Reps", y="Exercise_Name", orientation="h",
                     color="Reps", color_continuous_scale=["#00D9F5", "#00F5A0"],
                     title="Top 10 Exercises by Total Reps")
        fig.update_layout(**PLOT_LAYOUT, coloraxis_showscale=False)
        fig.update_xaxes(gridcolor="rgba(255,255,255,0.05)")
        fig.update_yaxes(showgrid=False)
        st.plotly_chart(fig, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 4 — CONSISTENCY ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
elif page == "consistency":
    section("WORKOUT CONSISTENCY")

    if not df.empty:
        bd = best_day(df)
        md = most_skipped_day(df)
        cs = current_streak(df)
        wc = weekly_consistency(df)

        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(kpi("🏆", bd[:3], "Best Day"), unsafe_allow_html=True)
        c2.markdown(kpi("😴", md[:3], "Most Skipped"), unsafe_allow_html=True)
        c3.markdown(kpi("⚡", cs, "Longest Streak"), unsafe_allow_html=True)
        c4.markdown(kpi("📊", f"{wc}%", "Last 7 Days"), unsafe_allow_html=True)

        st.markdown("")
        st.plotly_chart(heatmap_chart(df), use_container_width=True)

        c5, c6 = st.columns(2)
        with c5:
            st.plotly_chart(weekly_activity_chart(df), use_container_width=True)
        with c6:
            # Monthly bar
            df2 = df.copy()
            df2["Month"] = df2["Date"].dt.to_period("M").astype(str)
            monthly = df2.groupby("Month")["Workout_Completed"].sum().reset_index()
            fig = px.line(monthly, x="Month", y="Workout_Completed",
                          title="Monthly Workout Count",
                          color_discrete_sequence=["#FFB347"])
            fig.update_traces(line_width=2.5, mode="lines+markers+text",
                              text=monthly["Workout_Completed"],
                              textposition="top center",
                              marker=dict(size=7, color="#FFB347"))
            fig.update_layout(**PLOT_LAYOUT)
            fig.update_xaxes(showgrid=False, tickangle=45)
            fig.update_yaxes(gridcolor="rgba(255,255,255,0.05)")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available.")


# ════════════════════════════════════════════════════════════════════════════
# PAGE 5 — BMI & BODY METRICS
# ════════════════════════════════════════════════════════════════════════════
elif page == "bmi":
    section("BMI & BODY METRICS")

    with st.expander("📐 Calculate Your BMI", expanded=True):
        c1, c2, c3 = st.columns(3)
        height_cm = c1.number_input("Height (cm)", min_value=100, max_value=250, value=175)
        weight_kg = c2.number_input("Weight (kg)", min_value=30, max_value=250, value=70)
        age       = c3.number_input("Age",          min_value=10, max_value=100, value=22)

        height_m = height_cm / 100
        bmi_calc = round(weight_kg / height_m**2, 1)
        cat, color = bmi_category(bmi_calc)

        st.markdown(f"""
        <div style='text-align:center; padding:20px; background:#12122A;
                     border:1px solid {color}; border-radius:12px; margin-top:16px;'>
            <div style='font-family:Orbitron,monospace; font-size:3rem; color:{color};'>{bmi_calc}</div>
            <div style='font-size:1.2rem; color:{color}; margin-top:8px;'>{cat}</div>
            <div style='color:#666; font-size:0.8rem; margin-top:6px;'>BMI = weight / height²</div>
        </div>
        """, unsafe_allow_html=True)

    section("BMI CATEGORIES")
    cats = [("< 18.5", "Underweight", C_ACCENT),
            ("18.5 – 24.9", "Normal ✅", C_PRIMARY),
            ("25 – 29.9", "Overweight", C_WARN),
            ("≥ 30", "Obese", C_DANGER)]
    cols = st.columns(4)
    for col, (rng, name, clr) in zip(cols, cats):
        col.markdown(f"""<div class="kpi-card" style="border-color:{clr}40;">
            <span class="kpi-value" style="color:{clr}; font-size:1.3rem;">{rng}</span>
            <span class="kpi-label">{name}</span>
        </div>""", unsafe_allow_html=True)

    if not df.empty:
        section("WEIGHT TREND")
        st.plotly_chart(weight_trend_chart(df), use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 6 — SKILL PROGRESSION
# ════════════════════════════════════════════════════════════════════════════
elif page == "skills":
    section("SKILL PROGRESSION TRACKER")

    skill_vals = {}
    for sk in SKILLS:
        sub = df[df["Exercise_Name"] == sk] if not df.empty else pd.DataFrame()
        val = int(sub["Skill_Level"].mean()) if not sub.empty else random.randint(15, 55)
        skill_vals[sk] = val

    c_cols = st.columns(len(SKILLS))
    for col, (sk, val) in zip(c_cols, skill_vals.items()):
        clr = C_PRIMARY if val >= 70 else C_WARN if val >= 40 else C_DANGER
        col.markdown(f"""<div class="kpi-card">
            <span class="kpi-icon">🎯</span>
            <span class="kpi-value" style="color:{clr}; font-size:1.5rem;">{val}%</span>
            <span class="kpi-label">{sk}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("")
    for sk, val in skill_vals.items():
        progress_bar(sk, val)

    section("SKILL RADAR")
    st.plotly_chart(skill_radar_chart(df), use_container_width=True)

    section("MILESTONE TRACKER")
    milestones = {
        "Muscle Ups":             [(1, "First rep"), (3, "Triple"), (5, "5 clean"), (10, "Elite")],
        "Handstand Hold":         [(5, "5 sec"),     (15, "15 sec"), (30, "30 sec"), (60, "1 min")],
        "L-Sit":                  [(5, "5 sec"),     (10, "10 sec"), (20, "20 sec"), (30, "30 sec")],
        "Front Lever Progression":[(10, "Tuck"),     (20, "Adv Tuck"), (40, "Straddle"), (70, "Full")],
        "Planche Progression":    [(10, "Tuck"),     (25, "Adv Tuck"), (50, "Straddle"), (80, "Full")],
    }
    for sk, steps in milestones.items():
        val = skill_vals.get(sk, 0)
        cols = st.columns([2] + [1]*len(steps))
        cols[0].markdown(f"**{sk}**")
        for i, (threshold, label) in enumerate(steps):
            reached = "✅" if val >= threshold else "⬜"
            cols[i+1].markdown(f"{reached} {label}")


# ════════════════════════════════════════════════════════════════════════════
# PAGE 7 — RECOMMENDATIONS
# ════════════════════════════════════════════════════════════════════════════
elif page == "reco":
    section("WORKOUT RECOMMENDATIONS")

    level_sel = st.selectbox("Your Level", ["Beginner", "Intermediate", "Advanced"])
    user_df = df[df["User_Level"] == level_sel] if not df.empty else pd.DataFrame()
    reco = get_recommendations(user_df, level_sel)

    st.markdown(f"""<div class="rec-card">
        <div style='font-size:1.1rem; color:#E0E0E0; line-height:1.6;'>{reco['message']}</div>
    </div>""", unsafe_allow_html=True)

    if reco["rest_day"]:
        st.balloons()
    else:
        section("TODAY'S RECOMMENDED EXERCISES")
        cols = st.columns(3)
        for i, ex in enumerate(reco["routine"]):
            info = EXERCISE_LIBRARY.get(ex, {})
            cols[i % 3].markdown(f"""<div class="lib-card">
                <div class="lib-title">💪 {ex}</div>
                <div class="lib-meta">🎯 {info.get('muscle','—')} &nbsp;|&nbsp; {info.get('reps','—')}</div>
                <div style='font-size:0.82rem; color:#aaa; margin-top:8px;'>{info.get('tip','')}</div>
            </div>""", unsafe_allow_html=True)

        if reco["focus"]:
            st.info(f"🎯 **Focus area today:** {reco['focus']} — your weakest group based on history.")

    section("LEVEL-SPECIFIC ROUTINES")
    tab_b, tab_i, tab_a = st.tabs(["🟢 Beginner", "🟡 Intermediate", "🔴 Advanced"])
    with tab_b:
        st.markdown("**Warm-up → Upper → Core → Lower → Cool-down**")
        for ex in ["Incline Pushups", "Squats", "Plank", "Leg Raises", "Lunges", "Glute Bridge"]:
            info = EXERCISE_LIBRARY.get(ex, {})
            st.markdown(f"- **{ex}** — {info.get('reps','—')} &nbsp;|&nbsp; _{info.get('tip','')}_")
    with tab_i:
        for ex in ["Standard Pushups", "Pullups", "Dips", "Jump Squats", "Hollow Hold", "Russian Twists"]:
            info = EXERCISE_LIBRARY.get(ex, {})
            st.markdown(f"- **{ex}** — {info.get('reps','—')} &nbsp;|&nbsp; _{info.get('tip','')}_")
    with tab_a:
        for ex in ["Muscle Ups", "Handstand Pushups", "Dragon Flag", "Pistol Squats", "L-Sit", "Planche Progression"]:
            info = EXERCISE_LIBRARY.get(ex, {})
            st.markdown(f"- **{ex}** — {info.get('reps','—')} &nbsp;|&nbsp; _{info.get('tip','')}_")


# ════════════════════════════════════════════════════════════════════════════
# PAGE 8 — CALORIE & PERFORMANCE ANALYTICS
# ════════════════════════════════════════════════════════════════════════════
elif page == "calories":
    section("CALORIE & PERFORMANCE ANALYTICS")

    if not df.empty:
        tc    = total_calories(df)
        wc_cal = df[df["Date"] >= df["Date"].max() - pd.Timedelta(days=6)]["Calories_Burned"].sum()
        max_cal_row = df.loc[df["Calories_Burned"].idxmax()]
        avg_intensity = round(df["Calories_Burned"].mean(), 1)

        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(kpi("🔥", f"{wc_cal:,.0f}", "This Week (cal)"), unsafe_allow_html=True)
        c2.markdown(kpi("📆", f"{tc:,.0f}", "All-Time (cal)"),      unsafe_allow_html=True)
        c3.markdown(kpi("🏆", max_cal_row["Exercise_Name"][:8], "Best Exercise"), unsafe_allow_html=True)
        c4.markdown(kpi("⚡", avg_intensity, "Avg Cal/Entry"),       unsafe_allow_html=True)

        st.markdown("")
        c5, c6 = st.columns(2)
        with c5:
            st.plotly_chart(calories_pie(df), use_container_width=True)
        with c6:
            st.plotly_chart(monthly_calories_bar(df), use_container_width=True)

        st.plotly_chart(calories_trend_chart(df), use_container_width=True)

        section("TOP CALORIE-BURNING EXERCISES")
        top_cal = df.groupby("Exercise_Name")["Calories_Burned"].sum().nlargest(8).reset_index()
        fig = px.bar(top_cal, x="Exercise_Name", y="Calories_Burned",
                     color="Calories_Burned",
                     color_continuous_scale=["#FFB347", "#FF6B6B"],
                     title="Top Exercises by Calories Burned")
        fig.update_layout(**PLOT_LAYOUT, coloraxis_showscale=False)
        fig.update_xaxes(showgrid=False, tickangle=30)
        fig.update_yaxes(gridcolor="rgba(255,255,255,0.05)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available.")


# ════════════════════════════════════════════════════════════════════════════
# PAGE 9 — EXERCISE LIBRARY
# ════════════════════════════════════════════════════════════════════════════
elif page == "library":
    section("EXERCISE LIBRARY")

    search = st.text_input("🔍 Search exercises...", placeholder="e.g. pushup, pullup, plank")
    lvl_filter = st.multiselect("Filter by Level", ["Beginner", "Intermediate", "Advanced"],
                                 default=["Beginner", "Intermediate", "Advanced"])

    filtered = {k: v for k, v in EXERCISE_LIBRARY.items()
                if (search.lower() in k.lower() or search == "")
                and v["level"] in lvl_filter}

    st.markdown(f"<div style='color:#666; font-size:0.82rem; margin-bottom:16px;'>Showing {len(filtered)} exercises</div>",
                unsafe_allow_html=True)

    badge_cls = {"Beginner": "", "Intermediate": "inter", "Advanced": "adv"}

    cols = st.columns(3)
    for i, (ex, info) in enumerate(filtered.items()):
        cls = badge_cls.get(info["level"], "")
        cols[i % 3].markdown(f"""
        <div class="lib-card">
            <div class="lib-title">{ex}</div>
            <span class="ex-badge {cls}">{info['level']}</span>
            <div class="lib-meta" style="margin-top:10px;">
                🎯 <b>Muscle:</b> {info['muscle']}<br>
                🔢 <b>Reps:</b> {info['reps']}<br>
                💡 {info['tip']}
            </div>
        </div>
        """, unsafe_allow_html=True)

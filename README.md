# ⚡ CaliFit — Calisthenics Progress Dashboard

> A modern, interactive fitness analytics platform built with Streamlit
> **DVT Project | B.Tech 2025**

---

## 📌 Project Overview

**CaliFit** is a full-featured calisthenics tracking and analytics dashboard that helps athletes at all levels — Beginner, Intermediate, and Advanced — monitor their workout consistency, track strength progression, visualize body metrics, and receive smart workout recommendations.

Built as a Data Visualization Techniques (DVT) project, it demonstrates real-world use of Python data tools including Pandas, NumPy, Plotly, and Streamlit.

---

## 🚀 Features

| Page | Description |
|------|-------------|
| 🏠 Home Dashboard | KPI cards, summary stats, weekly consistency |
| 📋 Workout Tracker | Log workouts; saves to CSV |
| 📈 Progress Analytics | Strength charts, reps over time, volume breakdown |
| 🔥 Consistency Analysis | Heatmaps, streaks, best/worst days |
| ⚖️ BMI & Body Metrics | BMI calculator, weight trend chart |
| 🎯 Skill Progression | Radar chart, milestone tracker for advanced skills |
| 🤖 Recommendations | Rule-based engine suggests next workout |
| 🔥 Calorie Analytics | Pie charts, monthly trends, top exercises |
| 📚 Exercise Library | Searchable database of 40+ exercises with tips |

---

## 🛠️ Technologies Used

- **Python 3.10+**
- **Streamlit** — Dashboard framework
- **Pandas / NumPy** — Data processing
- **Plotly** — Interactive charts (line, bar, pie, heatmap, radar)
- **Matplotlib / Seaborn** — Static visualizations (optional)

---

## 📦 Installation

```bash
# 1. Clone / download the project
cd calisthenics-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate sample data (run once)
python generate_data.py

# 4. Launch the dashboard
streamlit run app.py
```

Open your browser at **http://localhost:8501**

---

## 📁 Folder Structure

```
calisthenics-dashboard/
│
├── data/
│   └── workouts.csv          ← Generated/sample workout dataset
│
├── assets/
│   └── images/               ← Optional screenshots
│
├── app.py                    ← Main Streamlit dashboard
├── analytics.py              ← Chart & data helper functions
├── recommendation.py         ← Rule-based recommendation engine
├── generate_data.py          ← Sample data generator
├── requirements.txt
└── README.md
```

---

## 📊 Dashboard Screenshots

_(Add screenshots after running the app)_

- Home Dashboard with KPI cards
- Workout heatmap
- Skill radar chart
- Exercise library search

---

## 🔮 Future Scope

- Multi-user login system with authentication
- PDF report export
- AI-powered exercise suggestions (LLM integration)
- Mobile app version (React Native)
- Wearable device data sync
- Achievement badges and gamification
- Push notifications / workout reminders

---

## ⚠️ Data and status

The included CSV is a generated/sample dataset. The dashboard writes newly
entered rows to the local CSV and has no authentication or multi-user storage.
Do not use it for medical decisions or place private workout data in a public
repository. This remains an academic/demo project; no production deployment is
configured.

## 📄 License

No license is currently supplied. Confirm the intended distribution terms before
sharing a public repository.

## 🏗️ Architecture

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the data flow and local storage boundary.

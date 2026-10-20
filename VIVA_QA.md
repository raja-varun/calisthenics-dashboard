# 🎓 VIVA QUESTIONS & ANSWERS
## Calisthenics Progress Dashboard — DVT Project

---

### 1. What is Data Visualization?
**A:** Data Visualization is the graphical representation of information and data using visual elements like charts, graphs, and maps. It helps identify patterns, trends, and outliers in large datasets that would be hard to see in raw form.

---

### 2. Why did you choose Streamlit for this project?
**A:** Streamlit is a Python-based open-source framework that allows building interactive web dashboards quickly without requiring HTML/CSS/JavaScript knowledge. It's ideal for data science projects because it integrates natively with Pandas, Plotly, and NumPy, and supports rapid prototyping.

---

### 3. What is Plotly and why is it used here?
**A:** Plotly is an interactive charting library for Python. Unlike Matplotlib, Plotly charts support zooming, panning, hover tooltips, and are fully responsive. We use it for line charts, bar charts, pie charts, radar charts, and heatmaps in this dashboard.

---

### 4. What is a KPI card?
**A:** KPI stands for Key Performance Indicator. A KPI card is a compact UI element that displays a single important metric prominently — like total workouts completed, calories burned, or current streak. It gives users an at-a-glance summary of performance.

---

### 5. How is BMI calculated?
**A:** BMI (Body Mass Index) is calculated as:
```
BMI = Weight (kg) / Height² (m²)
```
Categories:
- < 18.5 → Underweight
- 18.5 – 24.9 → Normal
- 25 – 29.9 → Overweight
- ≥ 30 → Obese

---

### 6. What is a Heatmap and how is it used in this project?
**A:** A heatmap is a 2D visualization where color intensity represents the magnitude of values. In this project, we use a heatmap to visualize workout frequency across days of the week vs weeks of the year — darker green = more workouts on that day.

---

### 7. What is a Radar Chart?
**A:** A radar (spider) chart displays multivariate data on a 2D chart with 3+ axes radiating from the center. In this project, it visualizes progress across multiple advanced calisthenics skills simultaneously — Muscle Ups, Handstand, L-Sit, Front Lever, Planche.

---

### 8. Explain the recommendation system used.
**A:** The recommendation engine is rule-based (no AI/ML). It analyzes:
1. Days worked out in the last 7 days (if ≥ 6, recommends rest)
2. Average reps per muscle group (recommends the weakest group)
3. Specific exercise averages (e.g., if Pullup avg < 5 reps, recommends Assisted Pullups)

This approach is simple, transparent, and effective for a beginner-friendly application.

---

### 9. How is the workout streak calculated?
**A:** The streak counter increments by 1 each day the user logs at least one workout. It resets to 0 on any day with no workout logged. The maximum streak value across the dataset is displayed as the longest streak.

---

### 10. What is the difference between Matplotlib and Plotly?
**A:**
| Feature | Matplotlib | Plotly |
|---------|-----------|--------|
| Interactivity | Static | Interactive (hover, zoom, pan) |
| Learning curve | Moderate | Easy |
| Web integration | Poor | Excellent |
| Chart types | Basic | Rich (3D, maps, etc.) |

We primarily use Plotly for its interactivity in the web dashboard.

---

### 11. What is Pandas and how is it used here?
**A:** Pandas is a Python library for data manipulation and analysis. In this project, it's used to:
- Load the CSV workout dataset
- Filter data by user, level, and date
- Group and aggregate data for charts (groupby, sum, mean)
- Add new workout entries to the CSV

---

### 12. What is a consistency score?
**A:** Weekly consistency score = (Number of days with a workout in last 7 days / 7) × 100. For example, if a user worked out 5 out of 7 days, the score is 71.4%.

---

### 13. Why use CSV for data storage instead of a database?
**A:** For this academic project, CSV is used because:
- It's simple and requires no setup
- Pandas reads/writes CSV natively
- Suitable for single-user demo use
In production, a database like SQLite or PostgreSQL would be preferred for multi-user support and data integrity.

---

### 14. What are the key visualizations in your dashboard?
**A:**
1. **Line Chart** — Exercise reps over time (progress tracking)
2. **Area Chart** — Calories burned daily trend
3. **Bar Chart** — Calories by muscle group, top exercises
4. **Pie/Donut Chart** — Calorie distribution by category
5. **Heatmap** — Workout frequency by day of week
6. **Radar Chart** — Skill progression across 5 skills
7. **KPI Cards** — Summary metrics at a glance
8. **Progress Bars** — Skill completion percentages

---

### 15. What are the future improvements you would add?
**A:**
- User authentication (login/logout per user)
- Machine learning-based workout recommendations
- PDF report export for progress
- Integration with wearable devices (Fitbit, Apple Watch)
- Achievement badge system for motivation
- Mobile-responsive PWA version

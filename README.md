# smart-study-planner

# 🌸 Smart Study Planner

A Flask-based study planning web application that helps students organize subjects, topics, exam dates, and available study time.

The application uses a priority-based scheduling algorithm to generate a personalized daily study plan based on exam urgency, subject difficulty, and preparation level.

## ✨ Features

- 📚 Add and manage subjects
- 📖 Add chapters and topics
- ✅ Track topic completion
- 📊 Record preparation level
- 🔥 Set subject difficulty
- 📅 Add exam dates
- ⏱️ Set available study hours
- 🧠 Generate a personalized study plan
- 📌 Prioritize subjects based on urgency, difficulty, and preparation
- 🎨 Student-friendly dashboard

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **Database:** SQLite
- **Scheduling:** Python-based priority algorithm

## 📂 Project Structure

```text
smart-study-planner/
│
├── app.py
├── requirements.txt
│
├── database/
│   └── db.py
│
├── scheduler/
│   └── planner.py
│
├── ml/
│   └── model.py
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── dashboard.html
│   ├── add_subject.html
│   ├── subject.html
│   └── settings.html
│
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── script.js

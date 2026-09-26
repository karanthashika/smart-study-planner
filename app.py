from flask import Flask, render_template, request, redirect

from database.db import init_db, get_db_connection
from scheduler.planner import generate_schedule


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    conn = get_db_connection()

    user = conn.execute(
        """
        SELECT study_hours
        FROM users
        WHERE id = ?
        """,
        (1,)
    ).fetchone()

    subjects = conn.execute(
        """
        SELECT subjects.*, exams.exam_date
        FROM subjects
        LEFT JOIN exams
        ON subjects.id = exams.subject_id
        WHERE subjects.user_id = ?
        ORDER BY subjects.id
        """,
        (1,)
    ).fetchall()

    conn.close()

    # Generate smart study schedule
    schedule = generate_schedule(
        subjects,
        user["study_hours"]
    )

    return render_template(
        "dashboard.html",
        subjects=subjects,
        study_hours=user["study_hours"],
        schedule=schedule
    )

    conn = get_db_connection()

    user = conn.execute(
        """
        SELECT study_hours
        FROM users
        WHERE id = ?
        """,
        (1,)
    ).fetchone()

    subjects = conn.execute(
        """
        SELECT subjects.*, exams.exam_date
        FROM subjects
        LEFT JOIN exams
        ON subjects.id = exams.subject_id
        WHERE subjects.user_id = ?
        ORDER BY subjects.id
        """,
        (1,)
    ).fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        subjects=subjects,
        study_hours=user["study_hours"]
    )


@app.route("/add-subject", methods=["GET", "POST"])
def add_subject():

    if request.method == "POST":

        subject_name = request.form["subject_name"]
        difficulty = int(request.form["difficulty"])
        preparation = int(request.form["preparation"])

        conn = get_db_connection()

        conn.execute(
            """
            INSERT INTO subjects
            (user_id, name, difficulty, preparation)
            VALUES (?, ?, ?, ?)
            """,
            (
                1,
                subject_name,
                difficulty,
                preparation
            )
        )

        conn.commit()
        conn.close()

        return redirect("/dashboard")

    return render_template("add_subject.html")


@app.route("/subject/<int:subject_id>")
def subject_details(subject_id):

    conn = get_db_connection()

    subject = conn.execute(
        """
        SELECT subjects.*, exams.exam_date
        FROM subjects
        LEFT JOIN exams
        ON subjects.id = exams.subject_id
        WHERE subjects.id = ? AND subjects.user_id = ?
        """,
        (subject_id, 1)
    ).fetchone()

    if subject is None:
        conn.close()
        return "Subject not found", 404

    topics = conn.execute(
        """
        SELECT *
        FROM topics
        WHERE subject_id = ?
        ORDER BY id
        """,
        (subject_id,)
    ).fetchall()

    conn.close()

    return render_template(
        "subject.html",
        subject=subject,
        topics=topics
    )


@app.route("/subject/<int:subject_id>/add-topic", methods=["POST"])
def add_topic(subject_id):

    topic_name = request.form["topic_name"].strip()

    if topic_name:

        conn = get_db_connection()

        subject = conn.execute(
            """
            SELECT *
            FROM subjects
            WHERE id = ? AND user_id = ?
            """,
            (subject_id, 1)
        ).fetchone()

        if subject is None:
            conn.close()
            return "Subject not found", 404

        conn.execute(
            """
            INSERT INTO topics
            (subject_id, name)
            VALUES (?, ?)
            """,
            (
                subject_id,
                topic_name
            )
        )

        conn.commit()
        conn.close()

    return redirect(f"/subject/{subject_id}")


@app.route("/topic/<int:topic_id>/toggle", methods=["POST"])
def toggle_topic(topic_id):

    conn = get_db_connection()

    topic = conn.execute(
        """
        SELECT topics.*, subjects.user_id
        FROM topics
        JOIN subjects
        ON topics.subject_id = subjects.id
        WHERE topics.id = ?
        AND subjects.user_id = ?
        """,
        (topic_id, 1)
    ).fetchone()

    if topic is None:
        conn.close()
        return "Topic not found", 404

    new_status = 0 if topic["completed"] else 1

    conn.execute(
        """
        UPDATE topics
        SET completed = ?
        WHERE id = ?
        """,
        (
            new_status,
            topic_id
        )
    )

    conn.commit()

    subject_id = topic["subject_id"]

    conn.close()

    return redirect(f"/subject/{subject_id}")


@app.route("/subject/<int:subject_id>/add-exam", methods=["POST"])
def add_exam(subject_id):

    exam_date = request.form["exam_date"]

    conn = get_db_connection()

    subject = conn.execute(
        """
        SELECT *
        FROM subjects
        WHERE id = ? AND user_id = ?
        """,
        (subject_id, 1)
    ).fetchone()

    if subject is None:
        conn.close()
        return "Subject not found", 404

    conn.execute(
        """
        DELETE FROM exams
        WHERE subject_id = ? AND user_id = ?
        """,
        (subject_id, 1)
    )

    conn.execute(
        """
        INSERT INTO exams
        (user_id, subject_id, exam_date)
        VALUES (?, ?, ?)
        """,
        (
            1,
            subject_id,
            exam_date
        )
    )

    conn.commit()
    conn.close()

    return redirect(f"/subject/{subject_id}")


@app.route("/settings")
def settings():

    conn = get_db_connection()

    user = conn.execute(
        """
        SELECT study_hours
        FROM users
        WHERE id = ?
        """,
        (1,)
    ).fetchone()

    conn.close()

    return render_template(
        "settings.html",
        study_hours=user["study_hours"]
    )


@app.route("/save-study-hours", methods=["POST"])
def save_study_hours():

    study_hours = float(request.form["study_hours"])

    if study_hours < 0.5 or study_hours > 12:
        return "Study hours must be between 0.5 and 12.", 400

    conn = get_db_connection()

    conn.execute(
        """
        UPDATE users
        SET study_hours = ?
        WHERE id = ?
        """,
        (study_hours, 1)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")


@app.route("/test-scheduler")
def test_scheduler():

    conn = get_db_connection()

    subjects = conn.execute(
        """
        SELECT subjects.*, exams.exam_date
        FROM subjects
        LEFT JOIN exams
        ON subjects.id = exams.subject_id
        WHERE subjects.user_id = ?
        """,
        (1,)
    ).fetchall()

    user = conn.execute(
        """
        SELECT study_hours
        FROM users
        WHERE id = ?
        """,
        (1,)
    ).fetchone()

    conn.close()

    schedule = generate_schedule(
        subjects,
        user["study_hours"]
    )

    return {
        "study_hours": user["study_hours"],
        "schedule": schedule
    }


if __name__ == "__main__":

    init_db()

    app.run(debug=True)
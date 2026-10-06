
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app = Flask(__name__)

# -----------------------------
# Configuration
# -----------------------------

app.config["SECRET_KEY"] = "taskflow-secret-key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///taskflow.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# -----------------------------
# Task Database Model
# -----------------------------

class Task(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    priority = db.Column(
        db.String(20),
        nullable=False,
        default="Medium"
    )

    category = db.Column(
        db.String(50),
        nullable=False,
        default="DevOps"
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="pending"
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    due_date = db.Column(
        db.String(20),
        nullable=False
    )

    due_time = db.Column(
        db.String(20),
        nullable=True
    )

    completed_at = db.Column(
        db.DateTime,
        nullable=True
    )


# -----------------------------
# Dashboard
# -----------------------------

@app.route("/")
def dashboard():

    tasks = Task.query.order_by(
        Task.created_at.desc()
    ).all()

    total_tasks = Task.query.count()

    completed_tasks = Task.query.filter_by(
        status="completed"
    ).count()

    pending_tasks = Task.query.filter_by(
        status="pending"
    ).count()

    today = date.today().isoformat()

    overdue_tasks = Task.query.filter(
        Task.status == "pending",
        Task.due_date < today
    ).count()

    return render_template(
        "dashboard.html",
        tasks=tasks,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        overdue_tasks=overdue_tasks
    )


# -----------------------------
# Create Task
# -----------------------------

@app.route(
    "/task/create",
    methods=["GET", "POST"]
)
def create_task():

    if request.method == "POST":

        title = request.form.get("title")
        description = request.form.get("description")

        priority = request.form.get(
            "priority",
            "Medium"
        )

        category = request.form.get(
            "category",
            "DevOps"
        )

        due_date = request.form.get("due_date")
        due_time = request.form.get("due_time")

        if not title or not due_date:

            flash(
                "Task title and due date are required."
            )

            return redirect(
                url_for("create_task")
            )

        task = Task(
            title=title,
            description=description,
            priority=priority,
            category=category,
            due_date=due_date,
            due_time=due_time
        )

        db.session.add(task)
        db.session.commit()

        flash("Task created successfully!")

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "task_form.html"
    )


# -----------------------------
# Edit Task
# -----------------------------

@app.route(
    "/task/<int:task_id>/edit",
    methods=["GET", "POST"]
)
def edit_task(task_id):

    task = db.get_or_404(
        Task,
        task_id
    )

    if request.method == "POST":

        task.title = request.form.get(
            "title"
        )

        task.description = request.form.get(
            "description"
        )

        task.priority = request.form.get(
            "priority"
        )

        task.category = request.form.get(
            "category"
        )

        task.due_date = request.form.get(
            "due_date"
        )

        task.due_time = request.form.get(
            "due_time"
        )

        db.session.commit()

        flash("Task updated successfully!")

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "task_form.html",
        task=task
    )


# -----------------------------
# Complete Task
# -----------------------------

@app.route(
    "/task/<int:task_id>/complete",
    methods=["POST"]
)
def complete_task(task_id):

    task = db.get_or_404(
        Task,
        task_id
    )

    task.status = "completed"

    task.completed_at = datetime.utcnow()

    db.session.commit()

    flash("Task completed!")

    return redirect(
        url_for("dashboard")
    )


# -----------------------------
# Delete Task
# -----------------------------

@app.route(
    "/task/<int:task_id>/delete",
    methods=["POST"]
)
def delete_task(task_id):

    task = db.get_or_404(
        Task,
        task_id
    )

    db.session.delete(task)

    db.session.commit()

    flash("Task deleted successfully!")

    return redirect(
        url_for("dashboard")
    )


# -----------------------------
# Health Check
# -----------------------------

@app.route("/health")
def health():

    return {
        "status": "healthy",
        "application": "TaskFlow"
    }


# -----------------------------
# Create Database
# -----------------------------

with app.app_context():
    db.create_all()


# -----------------------------
# Start Application
# -----------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )



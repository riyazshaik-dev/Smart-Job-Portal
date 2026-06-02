from flask import Flask, render_template, request, redirect, flash, send_from_directory
from werkzeug.utils import secure_filename
import os
import sqlite3
from flask import session

app = Flask(__name__)
app.secret_key = "secret123"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Database connection
import sqlite3
import os

def get_db():
    db_path = os.path.join(os.getcwd(), "database.db")
    print("Using DB:", db_path)   # 👈 DEBUG (important)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # ⭐ professional upgrade

    return conn


# Home page
@app.route("/")
def home():

    conn = get_db()

    jobs = conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
    applications = conn.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
    users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]

    return render_template(
        "index.html",
        total_jobs=jobs,
        total_applications=applications,
        total_users=users
    )


# Register page
import re   # 👈 ADD THIS AT TOP

@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        # 🔥 EMAIL VALIDATION (IMPORTANT)
        pattern = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'

        if not re.match(pattern, email):
            flash("Please enter a valid email address!")
            return redirect("/register")

        conn = get_db()

        conn.execute(
            "INSERT INTO users (name,email,password) VALUES (?,?,?)",
            (name,email,password)
        )

        conn.commit()

        flash("Registration successful!")
        return redirect("/login")

    return render_template("register.html")


# Login page
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        ).fetchone()

        if user:
            session["user_id"] = user[0]   # ⭐ important
            session["user_name"] = user[1]

            flash("Login successful!")
            return redirect("/jobs")

        else:
            flash("Invalid email or password")
            return redirect("/login")

    return render_template("login.html")
# Dashboard
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

#profile
@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()

    user = conn.execute(
        "SELECT * FROM users WHERE id=?",
        (session["user_id"],)
    ).fetchone()

    # 🔥 Count applications (user-specific)
    applications = conn.execute(
        "SELECT COUNT(*) FROM applications WHERE user_id=?",
        (session["user_id"],)
    ).fetchone()[0]

    # 🔥 Count saved jobs (user-specific)
    saved = conn.execute(
        "SELECT COUNT(*) FROM saved_jobs WHERE user_id=?",
        (session["user_id"],)
    ).fetchone()[0]

    return render_template(
        "profile.html",
        user=user,
        total_applications=applications,
        total_saved=saved
    )

# View jobs
@app.route("/jobs")
def jobs():

    search = request.args.get("search")
    category = request.args.get("category")

    conn = get_db()

    query = "SELECT * FROM jobs WHERE 1=1"
    params = []

    if search:
        query += " AND title LIKE ?"
        params.append('%' + search + '%')

    if category:
        query += " AND category=?"
        params.append(category)

    jobs = conn.execute(query, params).fetchall()

    return render_template("jobs.html", jobs=jobs, total=len(jobs))

@app.route("/saved_jobs")
def saved_jobs():

    if "user_id" not in session:
        flash("Please login first!")
        return redirect("/login")

    conn = get_db()

    jobs = conn.execute("""
        SELECT jobs.id,
               jobs.title,
               jobs.company
        FROM saved_jobs
        JOIN jobs ON jobs.id = saved_jobs.job_id
        WHERE saved_jobs.user_id=?
    """, (session["user_id"],)).fetchall()

    return render_template("saved_jobs.html", jobs=jobs)

@app.route("/save_job/<int:id>")
def save_job(id):

    if "user_id" not in session:
        flash("Please login first!")
        return redirect("/login")

    conn = get_db()

    existing = conn.execute(
        "SELECT * FROM saved_jobs WHERE job_id=? AND user_id=?",
        (id, session["user_id"])
    ).fetchone()

    if existing:
        flash("Job already saved!")

    else:
        conn.execute(
            "INSERT INTO saved_jobs (job_id,user_id) VALUES (?,?)",
            (id, session["user_id"])
        )

        conn.commit()

        flash("Job saved successfully!")

    return redirect("/jobs")# Job details


@app.route("/job/<int:id>")
def job_detail(id):

    conn = get_db()

    job = conn.execute(
        "SELECT * FROM jobs WHERE id=?",
        (id,)
    ).fetchone()

    return render_template("job_detail.html", job=job)


# Admin dashboard

@app.route("/admin")
def admin():

    conn = get_db()

    applications = conn.execute("""
        SELECT jobs.title, jobs.company, applications.resume, applications.status, applications.id
        FROM applications
        JOIN jobs ON jobs.id = applications.job_id
    """).fetchall()

    total = len(applications)

    return render_template("admin.html", applications=applications, total=total)

# My applications
@app.route("/my_applications")
def my_applications():

    if "user_id" not in session:
        flash("Please login first!")
        return redirect("/login")

    conn = get_db()

    applications = conn.execute("""
        SELECT jobs.title,
               jobs.company,
               applications.resume,
               applications.status
        FROM applications
        JOIN jobs ON jobs.id = applications.job_id
        WHERE applications.user_id=?
    """, (session["user_id"],)).fetchall()

    return render_template(
        "my_applications.html",
        applications=applications
    )

# Uploads
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory("uploads", filename)
# Logout
@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully!")

    return redirect("/")

# Post job
@app.route("/post_job", methods=["POST"])
def post_job():

    title = request.form["title"]
    company = request.form["company"]
    location = request.form["location"]
    salary = request.form["salary"]
    category = request.form["category"]
    description = request.form.get("description", "")

    conn = get_db()

    conn.execute(
        "INSERT INTO jobs (title,company,category,description,location,salary) VALUES (?,?,?,?,?,?)",
        (title, company, category, description, location, salary)
    )

    conn.commit()

    return redirect("/jobs")

# Delete job
@app.route("/delete_job/<int:id>")
def delete_job(id):

    conn = get_db()
    conn.execute("DELETE FROM jobs WHERE id=?", (id,))
    conn.commit()

    return redirect("/jobs")


# Update application status
@app.route("/update_status/<int:id>/<status>")
def update_status(id, status):

    conn = get_db()

    conn.execute(
        "UPDATE applications SET status=? WHERE id=?",
        (status, id)
    )

    conn.commit()

    return redirect("/admin")


# Apply job


@app.route("/apply/<int:job_id>", methods=["POST"])
def apply(job_id):

    # 🔐 Check login
    if "user_id" not in session:
        flash("Please login first!")
        return redirect("/login")

    conn = get_db()

    # 🔍 Check if THIS USER already applied
    existing = conn.execute(
        "SELECT * FROM applications WHERE job_id=? AND user_id=?",
        (job_id, session["user_id"])
    ).fetchone()

    if existing:
        flash("You already applied for this job!")

    else:
        file = request.files["resume"]

        if file and file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
        else:
            filename = None

        # ✅ Insert with user_id
        conn.execute(
            "INSERT INTO applications (job_id,resume,status,user_id) VALUES (?,?,?,?)",
            (job_id, filename, "pending", session["user_id"])
        )

        conn.commit()

        flash("Application submitted successfully!")

    return redirect("/jobs")

import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
from flask import Flask, render_template, request

app = Flask(__name__)

students = {
    "STU001": {
        "name": "John Doe",
        "department": "Computer Engineering",
        "level": "300"
    }
}


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        student_id = request.form.get("student_id", "").strip().upper()

        student = students.get(student_id)

        if student:
            return (
                f"Student Name: {student['name']}<br>"
                f"Department: {student['department']}<br>"
                f"Level: {student['level']}"
            )

        return "Student record not found.", 404

    return render_template("results.html")
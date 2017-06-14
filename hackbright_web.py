"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    return render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template('student_search.html')

@app.route("/student-add", methods=['GET'])
def student_add():
    """Add a student."""

    return render_template('student-add.html')


@app.route("/student-form-display", methods=['POST'])
def student_form_display():
    """Returns message that new student is added."""

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    github = request.form.get("github")

    QUERY = """ INSERT INTO hackbright (first_name, last_name, github)
              VALUES (:first_name, :last_name, :github)
              """
    hackbright.db.session.execute(QUERY,
                        {'first_name': first_name,
                        'last_name': last_name,
                        'github': github})
    hackbright.db.session.commit()

    return "You've successfully added a student!"

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)

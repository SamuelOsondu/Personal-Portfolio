import re
import os
import smtplib
from flask import Flask, render_template, send_file, request, jsonify, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField
from werkzeug.utils import secure_filename
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

UPLOAD_FOLDER = 'static/project_image'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pass'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL",  "sqlite:///projects.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
Bootstrap(app)


# EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', 'EMAIL_PASSWORD')


@app.route("/")
def home():
    all_projects = db.session.query(Projects).all()
    return render_template("index.html", projects=all_projects)



class AddProject(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired()])
    project_title = StringField('Project Title', validators=[DataRequired()])
    project_description = TextAreaField('Item Description', render_kw={"rows": 10, "cols": 11}, validators=[DataRequired()])
    project_link = StringField('Project Title', validators=[DataRequired()])
    file = FileField('File', validators=[FileRequired()])
    submit = SubmitField('Add Item')


class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(250), nullable=False)
    project_title = db.Column(db.String(250), nullable=False)
    project_description = db.Column(db.String(250), nullable=False)
    project_link = db.Column(db.String(250), nullable=False)
    project_img = db.Column(db.String(250), nullable=False)
    submit = SubmitField('Add Project')

db.create_all()



# downloading the resume on request
@app.route('/download')
def download_resume():
    path = "Resume - Samuel Osondu.pdf"
    return send_file(path, as_attachment=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    form = AddProject()
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files.get('file')
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            new_project = Projects(
                project_name=request.form.get('project_name'),
                project_title = request.form.get('project_title'),
                project_description = request.form.get('project_description'),
                project_link = request.form.get('project_link'),
                project_img = file_path,

            )
            db.session.add(new_project)
            db.session.commit()
            return redirect(url_for('add_project'))

    return render_template("project.html", form=form)


# Processing and sending the email
@app.route('/send_mail', methods=["POST"])
def send_mail():
    email = request.form['contactEmail']
    msg = request.form['contactMessage']
    subject = request.form['contactSubject']
    name = request.form['contactName']
    message = f"Subject: {subject} \n\n A MESSAGE FROM YOUR WEBSITE \n\n {msg} \n From: {name} \n Email: {email}"

    if len(name) < 2:
        return jsonify({"error": "Please enter your name."})

    regex = re.compile(
        r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+"
        r"(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")

    if re.fullmatch(regex, email):
        pass

    else:
        return jsonify({"email": "Please enter a valid email address."})

    if len(msg) < 15:
        return jsonify({"error": "Please enter your message. It should have at least 15 characters."})

    with smtplib.SMTP_SSL("smtp.gmail.com") as connection:
        connection.login(user="samuelemailsend@gmail.com", password="iypzrlzfcdqfuejk")
        connection.sendmail(
            from_addr="samuelemailsend@gmail.com",
            to_addrs="samuelosondu.py@gmail.com",
            msg=message
        )

        return jsonify("OK")


if __name__ == "__main__":
    app.run(debug=True, threaded=True)

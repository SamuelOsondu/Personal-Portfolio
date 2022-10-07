import re
import os
import smtplib
from flask import Flask, render_template, send_file, request, jsonify

app = Flask(__name__)


# EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', 'EMAIL_PASSWORD')


@app.route("/")
def home():
    return render_template("index.html")


# downloading the resume on request
@app.route('/download')
def download_resume():
    path = "Samuel Osondu - Resume.pdf"
    return send_file(path, as_attachment=True)


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
        connection.login(user="samuelemailsend@gmail.com", password=EMAIL_PASSWORD)
        connection.sendmail(
            from_addr="samuelemailsend@gmail.com",
            to_addrs="samuelosondu.py@gmail.com",
            msg=message
        )

        return jsonify("OK")


if __name__ == "__main__":
    app.run(debug=True, threaded=True)

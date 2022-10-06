import smtplib
from flask import Flask, render_template, send_file, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/download')
def download_resume():
    path = "Samuel Osondu - Resume.pdf"
    return send_file(path, as_attachment=True)


@app.route('/', methods=["POST"])
def send_mail():
    name = request.form['contactName']
    email = request.form['contactEmail']
    message = f"Subject: {request.form['contactSubject']} \n\n {request.form['contactMessage']}"

    with smtplib.SMTP_SSL("smtp.gmail.com") as connection:
        connection.login(user="samuelemailsend@gmail.com", password="fqzvjxtycowglskn")
        connection.sendmail(
            from_addr="samuelemailsend@gmail.com",
            to_addrs="samuelosondu99@gmail.com",
            msg=message
        )



if __name__ == "__main__":
    app.run(debug=True, threaded=True)

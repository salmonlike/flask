import os
from flask import Flask, render_template, request, redirect, flash
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # フォーム送信メッセージ用

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        subject = "【MyPath】お問い合わせが届きました"
        body = f"名前: {name}\nメール: {email}\n内容:\n{message}"
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = email
        msg["To"] = "aandkofspade@gmail.com"

        try:
            smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            smtp_server.login(os.environ.get("EMAIL_USER"), os.environ.get("EMAIL_PASS"))
            smtp_server.send_message(msg)
            smtp_server.quit()
            flash("送信されました。ありがとうございます！")
        except Exception as e:
            flash(f"エラーが発生しました: {e}")

        return redirect("/")
    return render_template("index.html")

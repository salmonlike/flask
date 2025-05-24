import os
from flask import Flask, render_template, request, redirect, flash
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

app = Flask(__name__)
app.secret_key = "your_secret_key"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        subject = "【MyPath】お問い合わせが届きました"
        body    = f"名前: {name}\nメール: {email}\n内容:\n{message}"

        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = Header(subject, "utf-8")

        # From に日本語表示名が含まれる場合、Header でラップ＋str化して ASCII 安全に
        sender_addr  = os.environ.get("EMAIL_USER")
        display_name = str(Header("MyPathサイト", "utf-8"))
        msg["From"]  = formataddr((display_name, sender_addr))

        msg["To"]       = "aandkofspade@gmail.com"
        msg["Reply-To"] = email

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(os.environ.get("EMAIL_USER"), os.environ.get("EMAIL_PASS"))
                smtp.send_message(msg)

            flash("送信されました。ありがとうございます！")
        except Exception as e:
            flash(f"エラーが発生しました: {e}")

        return redirect("/")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

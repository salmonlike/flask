import os
from flask import Flask, render_template, request, redirect, flash
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # フォーム送信メッセージ用

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        subject = "【MyPath】お問い合わせが届きました"
        body    = f"名前: {name}\nメール: {email}\n内容:\n{message}"

# 本文：UTF-8
        msg = MIMEText(body, 'plain', 'utf-8')

# 件名：UTF-8
        msg['Subject'] = Header(subject, 'utf-8')

# From は Gmail アカウント（ASCII のみ）に固定
        sender_addr = os.environ.get("EMAIL_USER")          # 例: mypath.info@gmail.com
        msg['From']  = formataddr(("MyPathサイト", sender_addr))

# To は受信用アドレス（ASCII のみ）
        msg['To'] = "aandkofspade@gmail.com"

# 返信先にユーザーのメールを入れる（ここは通常 ASCII だけ）
        msg['Reply-To'] = email

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

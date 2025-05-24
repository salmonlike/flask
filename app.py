import os, smtplib
from flask import Flask, render_template, request, redirect, flash
from email.mime.text import MIMEText
from email.header import Header
from email.utils  import formataddr

def strip_nbsp(t:str) -> str:
    return t.replace('\u00A0', ' ').strip()

app = Flask(__name__)
app.secret_key = "your_secret_key"

@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        name    = strip_nbsp(request.form["name"])
        email   = strip_nbsp(request.form["email"])
        message = strip_nbsp(request.form["message"])

        subject = "【MyPath】お問い合わせが届きました"
        body    = f"名前: {name}\nメール: {email}\n内容:\n{message}"

        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = Header(subject, "utf-8")

        sender_addr  = strip_nbsp(os.environ.get("EMAIL_USER", ""))
        display_name = str(Header("MyPathサイト", "utf-8"))
        msg["From"]  = formataddr((display_name, sender_addr))

        msg["To"]       = "aandkofspade@gmail.com"
        msg["Reply-To"] = email

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(sender_addr, os.environ.get("EMAIL_PASS"))
                smtp.send_message(msg)
            flash("送信されました。ありがとうございます！")
        except Exception as e:
            # デバッグ用にヘッダー内容を表示すると原因特定が早い
            print("=== DEBUG HEADERS ===")
            for k,v in msg.items():
                print(k, repr(v))
            flash(f"エラーが発生しました: {e}")

        return redirect("/")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

# app.py  ― MyPathサイト お問い合わせフォーム付き Flask アプリ
import os
from flask import Flask, render_template, request, redirect, flash
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils  import formataddr

app = Flask(__name__)
app.secret_key = "your_secret_key"         # フラッシュメッセージ用

#──────────────────────────────────────────────#
#  ルート → フォーム表示／送信処理
#──────────────────────────────────────────────#
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # フォームの値を取得
        name    = request.form["name"]
        email   = request.form["email"]
        message = request.form["message"]

        # 件名・本文（どちらも日本語を含むので UTF-8）
        subject = "【MyPath】お問い合わせが届きました"
        body    = f"名前: {name}\nメール: {email}\n内容:\n{message}"

        # 本文を UTF-8 でエンコード
        msg = MIMEText(body, "plain", "utf-8")

        # 件名も UTF-8 でエンコード
        msg["Subject"] = Header(subject, "utf-8")

        # 送信元（From）― 表示名は UTF-8、メールアドレスは ASCII
        sender_addr  = os.environ.get("EMAIL_USER")    # 例: mypath.info@gmail.com
        display_name = str(Header("MyPathサイト", "utf-8"))
        msg["From"]  = formataddr((display_name, sender_addr))

        # 受信先（To）― ASCII だけ
        msg["To"] = "aandkofspade@gmail.com"

        # 返信先（Reply-To）にユーザーのメールアドレスを入れる
        msg["Reply-To"] = email

        # ───── SMTP 経由で送信 ─────
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(
                    os.environ.get("EMAIL_USER"),   # Gmail アカウント
                    os.environ.get("EMAIL_PASS")    # アプリパスワード
                )
                smtp.send_message(msg)

            flash("送信されました。ありがとうございます！")
        except Exception as e:
            flash(f"エラーが発生しました: {e}")

        return redirect("/")

    # GET: フォーム表示
    return render_template("index.html")

# ローカルでテストするとき用
if __name__ == "__main__":
    app.run(debug=True)

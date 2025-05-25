# app.py ― 4ページ構成（トップ / 会社概要 / 事業内容 / お問い合わせ）＋ メール送信機能
import os, smtplib
from flask import Flask, render_template, request, redirect, flash, url_for
from email.mime.text import MIMEText
from email.header import Header
from email.utils  import formataddr

# ───────────────────────── strip_nbsp: 見えない全角スペースを除去
def strip_nbsp(t: str) -> str:
    return t.replace('\u00A0', ' ').strip()

# ───────────────────────── Flask アプリ
app = Flask(__name__)
app.secret_key = "your_secret_key"          # フラッシュメッセージ用

# ───────────────────────── ① トップページ
@app.route("/")
def home():
    return render_template("index.html")

# ───────────────────────── ② 会社概要ページ
@app.route("/about")
def about():
    return render_template("about.html")

# ───────────────────────── ③ 事業内容ページ
@app.route("/services")
def services():
    return render_template("services.html")

# ───────────────────────── ④ お問い合わせページ（GET + POST）
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # ── フォーム入力値を取得（NBSP除去）
        name    = strip_nbsp(request.form["name"])
        email   = strip_nbsp(request.form["email"])
        message = strip_nbsp(request.form["message"])

        # ── メール本文と件名
        subject = "【MyPath】お問い合わせが届きました"
        body    = f"名前: {name}\nメール: {email}\n内容:\n{message}"

        # ── MIMEText（UTF-8）
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = Header(subject, "utf-8")

        # ── 差出人（From）
        sender_addr  = strip_nbsp(os.environ.get("EMAIL_USER", ""))
        display_name = str(Header(strip_nbsp("MyPathサイト"), "utf-8"))
        msg["From"]   = formataddr((display_name, sender_addr))

        # ── 宛先（To）+ 返信先（Reply-To）
        msg["To"]       = "aandkofspade@gmail.com"
        msg["Reply-To"] = email

        # ── 送信
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(sender_addr, os.environ.get("EMAIL_PASS"))
                smtp.send_message(msg)
            flash("送信されました。ありがとうございます！")
        except Exception as e:
            # デバッグ用ヘッダー出力
            print("=== DEBUG HEADERS ===")
            for k, v in msg.items():
                print(k, repr(v))
            flash(f"エラーが発生しました: {e}")

        return redirect(url_for("contact"))     # 送信後に同じページへリダイレクト
    # GET
    return render_template("contact.html")

# ───────────────────────── ローカルテスト用
# if __name__ == "__main__":
#     app.run(debug=True)

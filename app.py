"""
    Flask を用いたWebアプリケーションのサンプルです。
    画像が投稿できるSNSアプリを作成します。
"""
import os
from datetime import datetime
import sqlite3
from flask import Flask, render_template, request, flash, redirect

dbname = "database.db"

app = Flask(__name__)
app.secret_key = 'my-secret-key'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024


def get_ext(filename):
    return filename.rsplit('.', 1)[1].lower()


@app.route("/")
def index():
    # 一覧を取得.
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    sql = "SELECT filename, body, created_at FROM posts"
    rows = c.execute(sql)
    posts = []
    for row in rows:
        post = {
            "filename": row[0],
            "body": row[1],
            "created_at": row[2]
        }
        posts.append(post)
    conn.commit()
    conn.close()
    return render_template("index.html", posts=posts)


@app.route("/post", methods=["POST"])
def post():
    if request.method == "POST":
        body = request.form.get("body")
        file = request.files.get("file")
        if not body or not file:
            flash("本文とファイルを設定してください。")
            return redirect("/")
        # 画像を保存.
        filename = str(datetime.now().timestamp()) + "." + get_ext(file.filename)
        file.save(os.path.join('.', 'static', 'posts', filename))
        # DBに保存.
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        sql = "insert into posts (filename, body, created_at) values (?, ?, ?)"
        user = (filename, body, datetime.now())
        c.execute(sql, user)
        conn.commit()
        conn.close()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
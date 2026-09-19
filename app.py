import os
import mysql.connector
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect

load_dotenv()

app = Flask(__name__)


def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        port=int(os.getenv("MYSQLPORT", 3306)),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE")
    )


@app.route("/")
def home():

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM comments
        ORDER BY created_at DESC
    """)

    comments = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "index.html",
        comments=comments
    )


@app.route("/comment", methods=["POST"])
def add_comment():

    nama = request.form.get("nama")
    komentar = request.form.get("komentar")

    if nama and komentar:

        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO comments
            (nama, komentar)
            VALUES (%s, %s)
        """, (nama, komentar))

        db.commit()

        cursor.close()
        db.close()

    return redirect("/#contact")


if __name__ == "__main__":
    app.run(debug=True)
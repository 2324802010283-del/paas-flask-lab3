import os
import psycopg2
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")


def get_connection():
    return psycopg2.connect(
        DATABASE_URL,
        sslmode="require"
    )


HTML = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Cloud Database - Lab 3</title>
    <style>
        body {
            font-family: Arial;
            background: #eef4ff;
            padding: 30px;
        }
        .container {
            background: white;
            max-width: 950px;
            margin: auto;
            padding: 25px;
            border-radius: 12px;
        }
        h1 { color: #1565c0; text-align: center; }
        input {
            padding: 10px;
            margin: 5px;
        }
        button {
            padding: 9px 15px;
            background: #1565c0;
            color: white;
            border: none;
            cursor: pointer;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }
        th {
            background: #1565c0;
            color: white;
        }
        .delete {
            background: #dc3545;
        }
        .edit {
            background: #198754;
        }
    </style>
</head>
<body>
<div class="container">

    <h1>Cloud Database - Bài thực hành 3</h1>

    <h2>Thêm người dùng</h2>

    <form action="/add" method="POST">
        <input name="fullname" placeholder="Họ và tên" required>
        <input name="email" type="email" placeholder="Email" required>
        <input name="major" placeholder="Ngành học">
        <button type="submit">Thêm dữ liệu</button>
    </form>

    <h2>Danh sách người dùng</h2>

    <table>
        <tr>
            <th>ID</th>
            <th>Họ tên</th>
            <th>Email</th>
            <th>Ngành</th>
            <th>Thao tác</th>
        </tr>

        {% for u in users %}
        <tr>
            <td>{{ u[0] }}</td>
            <td>{{ u[1] }}</td>
            <td>{{ u[2] }}</td>
            <td>{{ u[3] or '' }}</td>
            <td>
                <form action="/update/{{ u[0] }}" method="POST">
                    <input name="fullname"
                           value="{{ u[1] }}"
                           required>
                    <input name="major"
                           value="{{ u[3] or '' }}">
                    <button class="edit">Sửa</button>
                </form>

                <form action="/delete/{{ u[0] }}"
                      method="POST">
                    <button class="delete">Xóa</button>
                </form>
            </td>
        </tr>
        {% endfor %}
    </table>

</div>
</body>
</html>
"""


@app.route("/")
def home():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, fullname, email, major
        FROM users
        ORDER BY id
    """)

    users = cur.fetchall()

    cur.close()
    conn.close()

    return render_template_string(HTML, users=users)


@app.route("/add", methods=["POST"])
def add_user():
    fullname = request.form["fullname"]
    email = request.form["email"]
    major = request.form.get("major", "")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO users (fullname, email, major)
        VALUES (%s, %s, %s)
    """, (fullname, email, major))

    conn.commit()
    cur.close()
    conn.close()

    return redirect("/")


@app.route("/update/<int:user_id>", methods=["POST"])
def update_user(user_id):
    fullname = request.form["fullname"]
    major = request.form.get("major", "")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE users
        SET fullname = %s, major = %s
        WHERE id = %s
    """, (fullname, major, user_id))

    conn.commit()
    cur.close()
    conn.close()

    return redirect("/")


@app.route("/delete/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM users
        WHERE id = %s
    """, (user_id,))

    conn.commit()
    cur.close()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

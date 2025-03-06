from flask import Flask, render_template, request, redirect, session, flash, url_for
import mariadb
import bcrypt

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database connection
def get_db_connection():
    return mariadb.connect(
        user="root",
        password="",
        host="localhost",
        database="pims_db"
    )

# User Login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode("utf-8"), user[1].encode("utf-8")):
            session["user_id"] = user[0]
            return redirect("/dashboard")
        else:
            flash("Invalid credentials", "danger")

    return render_template("login.html")

# Logout
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/")

# Dashboard (List Personal Info)
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, phone, address FROM personal_info WHERE user_id = %s", (session["user_id"],))
    info = cursor.fetchall()
    conn.close()

    return render_template("dashboard.html", info=info)

# Add Personal Info
@app.route("/add", methods=["GET", "POST"])
def add_info():
    if "user_id" not in session:
        return redirect("/")

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        address = request.form["address"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO personal_info (name, email, phone, address, user_id) VALUES (%s, %s, %s, %s, %s)",
                       (name, email, phone, address, session["user_id"]))
        conn.commit()
        conn.close()

        flash("Personal information added successfully!", "success")
        return redirect("/dashboard")

    return render_template("add_info.html")

# Update Personal Info
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_info(id):
    if "user_id" not in session:
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, phone, address FROM personal_info WHERE id = %s AND user_id = %s", (id, session["user_id"]))
    info = cursor.fetchone()

    if not info:
        return redirect("/dashboard")

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        address = request.form["address"]

        cursor.execute("UPDATE personal_info SET name = %s, email = %s, phone = %s, address = %s WHERE id = %s",
                       (name, email, phone, address, id))
        conn.commit()
        conn.close()

        flash("Personal information updated successfully!", "success")
        return redirect("/dashboard")

    conn.close()
    return render_template("edit_info.html", info=info)

# Delete Personal Info
@app.route("/delete/<int:id>")
def delete_info(id):
    if "user_id" not in session:
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM personal_info WHERE id = %s AND user_id = %s", (id, session["user_id"]))
    conn.commit()
    conn.close()

    flash("Personal information deleted successfully!", "success")
    return redirect("/dashboard")

if __name__ == "__main__":
    app.run(debug=True)

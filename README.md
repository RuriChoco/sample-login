-------------------------------------- FORK BY DION CARLO LOPEZ ---------------------------------------

Repo from Sir Cañete
----------------------------------------------------------------------------------------------------------------



-------------------------------------- C O D E     E X P L A N A T I O N ---------------------------------------

Importing Required Modules
----------------------------------------------------------------------------------------------------------------
from flask import Flask, render_template, request, redirect, session, flash, url_for
import mariadb
import bcrypt

Flask – The web framework used to build this application.
render_template – Renders HTML templates for displaying web pages.
request – Handles incoming data (e.g., form submissions).
redirect – Redirects users to different routes.
session – Stores user session data (e.g., login state).
flash – Displays one-time alert messages to users.
url_for – Generates URLs for different routes.
mariadb – Connects to and interacts with a MariaDB database.
bcrypt – Hashes and verifies passwords securely.
----------------------------------------------------------------------------------------------------------------

Flask Application Initialization
----------------------------------------------------------------------------------------------------------------
app = Flask(__name__)
app.secret_key = "your_secret_key"

app = Flask(__name__) – Creates an instance of the Flask application.
app.secret_key = "your_secret_key" – Sets a secret key used for securely managing sessions and flash messages.
----------------------------------------------------------------------------------------------------------------

Database Connection Function
----------------------------------------------------------------------------------------------------------------
def get_db_connection():
    return mariadb.connect(
        user="root",
        password="",
        host="localhost",
        database="pims_db"
    )

This function establishes a connection to the MariaDB database (pims_db).
Uses root as the user with an empty password (not secure for production!).
Returns the database connection object.
----------------------------------------------------------------------------------------------------------------

User Login Route
----------------------------------------------------------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def login():

Defines a route ("/") that supports GET and POST requests.
If the user visits the page (GET request), they see the login form.
If they submit login details (POST request), authentication is performed.
----------------------------------------------------------------------------------------------------------------

Handling Login Form Submission
----------------------------------------------------------------------------------------------------------------
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

Defines a route ("/") that supports GET and POST requests.
If the user visits the page (GET request), they see the login form.
If they submit login details (POST request), authentication is performed.
----------------------------------------------------------------------------------------------------------------

Handling Login Form Submission
----------------------------------------------------------------------------------------------------------------
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
Extracts username and password from the submitted login form.
----------------------------------------------------------------------------------------------------------------

Database Query for Authentication
----------------------------------------------------------------------------------------------------------------
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()
Connects to the database.
Queries the users table to get the user's id and stored password hash.
Closes the connection after fetching the data.
----------------------------------------------------------------------------------------------------------------

Password Verification
----------------------------------------------------------------------------------------------------------------
        if user and bcrypt.checkpw(password.encode("utf-8"), user[1].encode("utf-8")):
            session["user_id"] = user[0]
            return redirect("/dashboard")
        else:
            flash("Invalid credentials", "danger")
Verifies the password using bcrypt.checkpw(), which compares the entered password with the stored hash.
If valid, the user’s ID is stored in the session, and they are redirected to the dashboard.
Otherwise, an error message ("Invalid credentials") is flashed.
----------------------------------------------------------------------------------------------------------------

Rendering the Login Page
----------------------------------------------------------------------------------------------------------------
    return render_template("login.html")
If the request is a GET request or authentication fails, the login page is shown.
----------------------------------------------------------------------------------------------------------------

Logout Route
----------------------------------------------------------------------------------------------------------------
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/")

Removes the user from the session, effectively logging them out.
Redirects them to the login page.
----------------------------------------------------------------------------------------------------------------

Dashboard Route
----------------------------------------------------------------------------------------------------------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")

Checks if the user is logged in (by verifying if "user_id" exists in session).
If not, redirects them to the login page.
----------------------------------------------------------------------------------------------------------------

Fetching Personal Information
----------------------------------------------------------------------------------------------------------------
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, phone, address FROM personal_info WHERE user_id = %s", (session["user_id"],))
    info = cursor.fetchall()
    conn.close()
Queries the personal_info table for data related to the logged-in user.
Closes the connection after fetching the data.
----------------------------------------------------------------------------------------------------------------

Rendering the Dashboard
----------------------------------------------------------------------------------------------------------------
    return render_template("dashboard.html", info=info)
    
Passes the retrieved info data to dashboard.html for display.
----------------------------------------------------------------------------------------------------------------

Adding Personal Information
----------------------------------------------------------------------------------------------------------------
@app.route("/add", methods=["GET", "POST"])
def add_info():
    if "user_id" not in session:
        return redirect("/")

Ensures that only logged-in users can add personal info.
----------------------------------------------------------------------------------------------------------------

Handling Form Submission
----------------------------------------------------------------------------------------------------------------
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        address = request.form["address"]
Extracts the submitted personal details.
----------------------------------------------------------------------------------------------------------------

Database Insertion
----------------------------------------------------------------------------------------------------------------
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO personal_info (name, email, phone, address, user_id) VALUES (%s, %s, %s, %s, %s)",
                       (name, email, phone, address, session["user_id"]))
        conn.commit()
        conn.close()
Inserts the new personal info into the personal_info table.
----------------------------------------------------------------------------------------------------------------

Flash Success Message and Redirect
----------------------------------------------------------------------------------------------------------------
        flash("Personal information added successfully!", "success")
        return redirect("/dashboard")
Displays a success message and redirects to the dashboard.
----------------------------------------------------------------------------------------------------------------

Editing Personal Information
----------------------------------------------------------------------------------------------------------------
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_info(id):
    if "user_id" not in session:
        return redirect("/")

Users must be logged in to edit information.
----------------------------------------------------------------------------------------------------------------

Fetching Existing Data
----------------------------------------------------------------------------------------------------------------
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, phone, address FROM personal_info WHERE id = %s AND user_id = %s", (id, session["user_id"]))
    info = cursor.fetchone()
Retrieves the existing personal info to be edited.
----------------------------------------------------------------------------------------------------------------

Updating Data
----------------------------------------------------------------------------------------------------------------
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        address = request.form["address"]

        cursor.execute("UPDATE personal_info SET name = %s, email = %s, phone = %s, address = %s WHERE id = %s",
                       (name, email, phone, address, id))
        conn.commit()
        conn.close()
Updates the personal info in the database.
----------------------------------------------------------------------------------------------------------------

Redirecting with Success Message
----------------------------------------------------------------------------------------------------------------
        flash("Personal information updated successfully!", "success")
        return redirect("/dashboard")
Displays a message and redirects.
----------------------------------------------------------------------------------------------------------------

Deleting Personal Information
----------------------------------------------------------------------------------------------------------------
@app.route("/delete/<int:id>")
def delete_info(id):
    if "user_id" not in session:
        return redirect("/")

Ensures that only logged-in users can delete personal info.
----------------------------------------------------------------------------------------------------------------

Deleting Data from Database
----------------------------------------------------------------------------------------------------------------
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM personal_info WHERE id = %s AND user_id = %s", (id, session["user_id"]))
    conn.commit()
    conn.close()
Deletes the selected entry.
----------------------------------------------------------------------------------------------------------------

Redirecting
----------------------------------------------------------------------------------------------------------------
    flash("Personal information deleted successfully!", "success")
    return redirect("/dashboard")
Displays a success message and redirects.
----------------------------------------------------------------------------------------------------------------

Running the Flask Application
----------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)

Starts the Flask server with debug mode enabled.
----------------------------------------------------------------------------------------------------------------



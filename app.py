from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)


# -----------------------------
# Database Connection
# -----------------------------
def get_db_connection():
    return mysql.connector.connect(
        host="moviebooking-db.cfsoogm80jir.us-west-1.rds.amazonaws.com",
        user="admin",
        password="Chandra766181",
        database="moviebooking",
        port=3306
    )


# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# Movies Page
# -----------------------------
@app.route("/movies")
def movies():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("movies.html", movies=movies)


# -----------------------------
# Booking Page
# -----------------------------
@app.route("/booking", methods=["GET", "POST"])
def booking():

    if request.method == "POST":

        movie_id = request.form["movie_id"]
        customer_name = request.form["customer_name"]
        customer_email = request.form["customer_email"]
        booking_date = request.form["booking_date"]
        show_time = request.form["show_time"]
        seats = request.form["seats"]

        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute(
            """
            INSERT INTO bookings
            (
                movie_id,
                customer_name,
                customer_email,
                booking_date,
                show_time,
                seats
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                movie_id,
                customer_name,
                customer_email,
                booking_date,
                show_time,
                seats
            )
        )

        db.commit()

        cursor.close()
        db.close()

        return redirect("/confirmation")

    return render_template("booking.html")


# -----------------------------
# Confirmation Page
# -----------------------------
@app.route("/confirmation")
def confirmation():
    return render_template("confirmation.html")


# -----------------------------
# Start Flask
# -----------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

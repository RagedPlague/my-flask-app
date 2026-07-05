from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "beautify_with_jess.db"

# Service: Price,
services = {
    "Classic Lashes": 80,
    "Hybrid Lashes": 95,
    "Volume Lashes": 110,
    "Lash Lift": 70,
    "Brow Wax": 25,
    "Brow Tint": 20,
    "Makeup": 90
}


# ---------------------------------
# Create the database and tables
# ---------------------------------
def create_database():

    # Connect to the database
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # Create the bookings table if it does not already exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            service TEXT NOT NULL,
            booking_date TEXT NOT NULL,
            booking_time TEXT NOT NULL
        )
    """)

    # Create the enquiries table if it does not already exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# ---------------------------------
# Home Page
# ---------------------------------
@app.route("/")
def index():
    return render_template("index.html")


# ---------------------------------
# Services Page
# ---------------------------------
@app.route("/services")
def services_page():
    return render_template("services.html", services=services)


# ---------------------------------
# Gallery Page
# ---------------------------------
@app.route("/gallery")
def gallery():
    return render_template("gallery.html")


# ---------------------------------
# Booking Page
# ---------------------------------
@app.route("/booking")
def booking():
    return render_template("booking.html", services=services)


# ---------------------------------
# Save a booking to the database
# ---------------------------------
@app.route("/add_booking", methods=["POST"])
def add_booking():

    # Retrieve information entered by the customer
    customer_name = request.form["customer_name"]
    phone = request.form["phone"]
    email = request.form["email"]
    service = request.form["service"]
    booking_date = request.form["booking_date"]
    booking_time = request.form["booking_time"]

    # Connect to the database
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # Insert the booking into the bookings table
    cursor.execute("""
        INSERT INTO bookings
        (customer_name, phone, email, service, booking_date, booking_time)

        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        customer_name,
        phone,
        email,
        service,
        booking_date,
        booking_time
    ))

    connection.commit()
    connection.close()

    # Redirect the user to the confirmation page
    return redirect("/confirmation")


# ---------------------------------
# Confirmation Page
# ---------------------------------
@app.route("/confirmation")
def confirmation():
    return render_template("confirmation.html")


# ---------------------------------
# Contact Page
# ---------------------------------
@app.route("/contact")
def contact():
    return render_template("contact.html")


# ---------------------------------
# Save an enquiry to the database
# ---------------------------------
@app.route("/add_enquiry", methods=["POST"])
def add_enquiry():

    # Retrieve the customer's enquiry
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    # Connect to the database
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # Insert the enquiry into the enquiries table
    cursor.execute("""
        INSERT INTO enquiries
        (name, email, message)

        VALUES (?, ?, ?)
    """, (name, email, message))

    connection.commit()
    connection.close()

    return redirect("/")



if __name__ == "__main__":
    create_database()
    app.run(debug=True)
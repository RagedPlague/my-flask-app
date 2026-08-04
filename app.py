from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "beautify_with_jess.db"

# The layout for this is as follows... Service: Price,
# This data type is a DICTIONARY
services = {
    "Classic Lashes": 80,
    "Hybrid Lashes": 95,
    "Volume Lashes": 110,
    "Lash Lift": 70,
    "Brow Wax": 25,
    "Brow Tint": 20,
    "Makeup": 90
}

service_images = {
    "Classic Lashes": "classic_lash.jpg",
    "Hybrid Lashes": "hybrid_lash.jpg",
    "Volume Lashes": "volume_lash.jpg",
    "Lash Lift": "lash_lift.jpg",
    "Brow Wax": "brow_wax.jpg",
    "Brow Tint": "brow_tint.jpg",
    "Makeup": "makeup.jpg"
}

service_descriptions = {
    "Classic Lashes": "A natural, elegant lash look for everyday wear.",
    "Hybrid Lashes": "A blend of classic and volume lashes for extra fullness.",
    "Volume Lashes": "A bold, dramatic style with maximum volume.",
    "Lash Lift": "Lifts and curls your natural lashes for a longer-looking effect.",
    "Brow Wax": "Shapes and defines your brows for a clean finish.",
    "Brow Tint": "Enhances your brows with rich, long-lasting colour.",
    "Makeup": "Professional makeup tailored for any occasion."
}

# Create the ENQUIRIES database and tables
def init_db():

    #Connect to database & make enquiries table
    conn = sqlite3.connect('enquiries.db')
    cursor = conn.cursor()

    # Create the enquiries table if it does not already exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# Saves an enquiry to the ENQUIRIES database
@app.route('/submit', methods=['POST'])
def submit_enquiry():
    # Get data using the 'name' attributes from HTML form
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    #This opens the connection and auto-closes it when finished
    with sqlite3.connect('enquiries.db') as conn:
        cursor = conn.cursor()
        
        #Create the table here so it exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS enquiries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL
            )
        ''')
        
        # Insert the data
        cursor.execute(
            "INSERT INTO enquiries (name, email, message) VALUES (?, ?, ?)",
            (name, email, message)
        )
        conn.commit()

    # Reloads webpage before adding text so the text stays on the webpage
    # without taking you to a seperate, blank webpage
    return render_template("contact.html", success="Thank you! Your enquiry has been received.")


# Create the BOOKING database and tables
def init_db():

    # Connect to the database
    conn = sqlite3.connect('beautify_with_jess.db')
    cursor = conn.cursor()

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
    conn.commit()
    conn.close()


# Saves a booking to the BOOKING database
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
    conn = sqlite3.connect("beautify_with_jess.db")
    cursor = conn.cursor()

    # Insert the booking into the bookings table
    cursor.execute(
        """INSERT INTO bookings
        (customer_name, phone, email, service, booking_date, booking_time)
        VALUES (?, ?, ?, ?, ?, ?)""",
        (customer_name, phone, email, service, booking_date, booking_time)
    )

    # Save changes
    conn.commit()

    # Get the ID of the booking that was just added
    booking_id = cursor.lastrowid

    # Close the database connection
    conn.close()

    # Redirect to the confirmation page for this booking, using ID from database
    return redirect(f"/confirmation/{booking_id}")


# Confirmation page
@app.route("/confirmation/<int:booking_id>")
def confirmation(booking_id):

    # Connect to the database
    conn = sqlite3.connect("beautify_with_jess.db")
    cursor = conn.cursor()

    # Retrieve the booking with the matching ID
    cursor.execute(
        "SELECT * FROM bookings WHERE id = ?",
        (booking_id,)
    )

    booking = cursor.fetchone()

    # Close the database connection
    conn.close()

    # Send the booking data to confirmation.html
    return render_template("confirmation.html", booking=booking)


# Home Page
@app.route("/")
def index():
    return render_template("index.html")


# Services Page
@app.route("/services")
def services_page():
    return render_template("services.html", services=services, service_images=service_images, service_descriptions=service_descriptions)


# Gallery Page
@app.route("/gallery")
def gallery():
    return render_template("gallery.html")


# Booking Page
@app.route("/booking")
def booking():
    selected_service = request.args.get("service")

    return render_template("booking.html",services=services, selected_service=selected_service)


# Edit Booking Page
@app.route("/edit_booking/<int:booking_id>", methods=["GET", "POST"])
def edit_booking(booking_id):

    conn = sqlite3.connect("beautify_with_jess.db")
    cursor = conn.cursor()

    if request.method == "POST":

        # Get updated booking details from the form
        customer_name = request.form["customer_name"]
        phone = request.form["phone"]
        email = request.form["email"]
        service = request.form["service"]
        booking_date = request.form["booking_date"]
        booking_time = request.form["booking_time"]

        # Update the existing booking in the database
        cursor.execute("""
            UPDATE bookings
            SET 
                customer_name = ?,
                phone = ?,
                email = ?,
                service = ?,
                booking_date = ?,
                booking_time = ?
            WHERE id = ?
        """, (
            customer_name,
            phone,
            email,
            service,
            booking_date,
            booking_time,
            booking_id
        ))

        conn.commit()
        conn.close()

        # Redirect to confirmation page after saving changes
        return redirect(f"/confirmation/{booking_id}")


    else:

        # Retrieve the selected booking
        cursor.execute("""
            SELECT *
            FROM bookings
            WHERE id = ?
        """, (booking_id,))

        booking = cursor.fetchone()

        conn.close()

        return render_template(
            "edit_booking.html",
            booking=booking,
            services=services
        )


# Update Booking
@app.route("/update_booking/<int:booking_id>", methods=["POST"])
def update_booking(booking_id):

    # Retrieve the updated information
    customer_name = request.form["customer_name"]
    phone = request.form["phone"]
    email = request.form["email"]
    service = request.form["service"]
    booking_date = request.form["booking_date"]
    booking_time = request.form["booking_time"]

    # Connect to the database
    conn = sqlite3.connect("beautify_with_jess.db")
    cursor = conn.cursor()

    # Update the booking
    cursor.execute("""
        UPDATE bookings
        SET 
            -- Replaces [title] with the updated value (which uses '?' as a placeholder)
            customer_name = ?,
            phone = ?,
            email = ?,
            service = ?,
            booking_date = ?,
            booking_time = ?
        WHERE id = ?
    """, (
        customer_name,
        phone,
        email,
        service,
        booking_date,
        booking_time,
        booking_id
    ))

    conn.commit()
    conn.close()

    # Return to the confirmation page
    return redirect(f"/confirmation/{booking_id}")

# Contact Page
@app.route("/contact")
def contact():
    return render_template("contact.html")


# Meet Jess Page
@app.route("/meetjess")
def meetjess():
    return render_template("meetjess.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
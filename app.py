from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database Connection
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost', 
        user='root',
        password='Exoteric7465@',
        database='ticket_booking'
    )
    return connection

# Home route to display available buses and prices
@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM buses;')
    buses = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', buses=buses)

# Booking route to handle ticket purchase
@app.route('/book/<bus_id>', methods=['POST'])
def book_ticket(bus_id):
    passenger_name = request.form['name']
    passenger_email = request.form['email']
    # Store the booking in the database
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO bookings (bus_id, name, email) VALUES (%s, %s, %s)',
                   (bus_id, passenger_name, passenger_email))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

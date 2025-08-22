Travel Booking App (Python Tkinter + MySQL)

A desktop travel booking application built using Python(Tkinter GUI) and MySQL.
Features include user registration & login, fare calculation, trip booking & payment processing.

Features

User registration & login (passwords are hashed)

Ability to create/search trips & calculate fare

Ability to book a trip & save the payment

Uses MySQL for a persistent database

Basic UI using Tkinter

Project Structure 

portfolio/
├─ travel_booking.py
├─ requirements.txt
├─ README.md
├─ .env                    
└─ assets/                  

Quick Start

1. Prerequisites

Python 3.9+

MySQL Server (local or remote)

2. Clone & install

git clone https://github.com/<aminjasey2003-netizen>/portfolio.git
cd portfolio 
pip install -r requirements.txt

If you don't have a requirements.txt yet, create one using the following at minimum:

mysql-connector-python

3. Setup database

Create a .env file in the root directory that should NOT be committed:

DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=cta_travel

4. Create schema (sample)

Run this in MySQL (e.g., via mysql CLI or phpMyAdmin):

CREATE DATABASE IF NOT EXISTS cta_travel CHARACTER SET utf8mb4;\
USE cta_travel;

CREATE TABLE IF NOT EXISTS users (\
id INT AUTO_INCREMENT PRIMARY KEY,\
full_name VARCHAR(100) NOT NULL,\
email VARCHAR(120) UNIQUE,\
username VARCHAR(50) UNIQUE,\
password_hash VARCHAR(255) NOT NULL,\
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\
);

CREATE TABLE IF NOT EXISTS trips (\
id INT AUTO_INCREMENT PRIMARY KEY,\
origin VARCHAR(100) NOT NULL,\
destination VARCHAR(100) NOT NULL,\
base_fare DECIMAL(10,2) NOT NULL,\
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\
);

CREATE TABLE IF NOT EXISTS bookings (\
id INT AUTO_INCREMENT PRIMARY KEY,\
user_id INT NOT NULL,\
trip_id INT NOT NULL,\
passengers INT NOT NULL DEFAULT 1,\
total_fare DECIMAL(10,2) NOT NULL,\
status ENUM('PENDING','PAID','CANCELLED') DEFAULT 'PENDING',\
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\
FOREIGN KEY (user_id) REFERENCES users(id),\
FOREIGN KEY (trip_id) REFERENCES trips(id)\
);

CREATE TABLE IF NOT EXISTS payments (\
id INT AUTO_INCREMENT PRIMARY KEY,\
booking_id INT NOT NULL,\
amount DECIMAL(10,2) NOT NULL,\
method VARCHAR(50),\
paid_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\
FOREIGN KEY (booking_id) REFERENCES bookings(id)\
);

5. Run the app\
   python travel_booking.py

🔧 Environment & Security

Store DB credentials in .env (never hardcode secrets).

Add .env to .gitignore:

.gitignore

.env\
**pycache**/\
\*.pyc

 Future Improvements

Input validation & better error messages

Password hashing with bcrypt

Receipt export (PDF)

Role-based access (admin/operator)

Unit tests

Author

Lamin Jassey

Email: laminjasey2003@gmail.com

https://github.com/laminjasey2003-netizen

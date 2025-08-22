import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import mysql.connector
import random
import bcrypt
import re

# Color scheme
background = "#062830"
framebg = "#EDEDED"
framefg = "#06283D"
button_color = "#FFAA33"
header_color = "#343a40"

# Zone and Station Mapping
ZONES = {
    "1: Downtown Zone": [
        "Adohad", "Brunad", "Erean", "Elyot", "Ederif", "Holmer",
        "Kevia", "Marend", "Perinad", "Pryn", "Ruril", "Ryall",
        "Vertwall", "Zord"
    ],
    "2: Midtown Zone": [
        "Agralle", "Docia", "Garion", "Olodus", "Obeylyn", "Quthieh",
        "Ralith", "Riclya", "Riladia", "Stonyam", "stlas", "Wicyt", "", ""
    ],
    "3: Central Zone": [
        "Bylyn", "Centralla", "Frestin", "Jaund", "Lomil", "Ninia",
        "Rede", "Soth", "Tallan", "Yaen", "", "", "", ""
    ]
}

FARES = {
    "Adult": 2105,
    "Child": 1410,
    "Senior": 1025,
    "Student": 1750
}

def Generate_voucher():
    if not validate_travelers():
        return

    start_zone = start_zone_var.get()
    destination_zone = destination_zone_var.get()

    if not start_zone or not destination_zone:
        messagebox.showerror("Error", "Both starting and destination stations must be selected.")
        return

    start_zone_num = int(start_zone_var.get()[0])
    end_zone_num = int(destination_zone_var.get()[0])
    zones_traveled = abs(start_zone_num - end_zone_num) + 1

    adults = int(adult_var.get())
    children = int(child_var.get())
    seniors = int(senior_var.get())
    students = int(student_var.get())

    total_adult_fare = adults * FARES["Adult"] * zones_traveled
    total_child_fare = children * FARES["Child"] * zones_traveled
    total_senior_fare = seniors * FARES["Senior"] * zones_traveled
    total_student_fare = students * FARES["Student"] * zones_traveled

    total_fare = total_adult_fare + total_child_fare + total_senior_fare + total_student_fare
    total_travelers = adults + children + seniors + students

    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    voucher_window = tk.Toplevel(root)
    voucher_window.title("Travel Voucher")
    voucher_window.configure(bg=background)
    voucher_window.geometry("600x500")

    # Header
    header_label = tk.Label(
        voucher_window,
        text="TRAVEL VOUCHER",
        font=("Arial", 16, "bold"),
        bg=background,
        fg="white"
    )
    header_label.pack(pady=(20, 10))

    ticket_number = random.randint(1, 100)

    voucher_text = (
        f"Travel Voucher\n\n"
        f"Date and Time of Issue: {current_datetime}\n\n"
        f"Starting Zone: {start_zone}\n"
        f"Destination Zone: {destination_zone}\n"
        f"Zones Traveled: {zones_traveled}\n\n"
        f"Number of Travelers:\n"
        f"  Adults: {adults} (Fare: {total_adult_fare} CENTS)\n"
        f"  Children: {children} (Fare: {total_child_fare} CENTS)\n"
        f"  Seniors: {seniors} (Fare: {total_senior_fare} CENTS)\n"
        f"  Students: {students} (Fare: {total_student_fare} CENTS)\n\n"
        f"Total Travelers: {total_travelers}\n"
        f"Ticket Number: {ticket_number}\n"
        f"Total Fare: {total_fare} CENTS"
    )

    voucher_label = tk.Label(
        voucher_window,
        text=voucher_text,
        font=("Arial", 12),
        justify="left",
        bg=background,
        fg="white"
    )
    voucher_label.pack(pady=20, padx=20)

    button_frame = tk.Frame(voucher_window, bg=background)
    button_frame.pack(pady=20)

    tk.Button(
        button_frame,
        text="Update Booking",
        command=voucher_window.destroy,
        bg=button_color,
        width=15
    ).pack(side="left", padx=10)

    tk.Button(
        button_frame,
        text="Save",
        command=save_booking,
        bg=button_color,
        width=15
    ).pack(side="left", padx=10)

    tk.Button(
        button_frame,
        text="buy tickect",
        command=lambda: [voucher_window.destroy(), handle_payment(total_travelers, total_fare)],
        bg=button_color,
        width=15
    ).pack(side="left", padx=10)

def validate_travelers():
    try:
        adults = int(adult_var.get())
        children = int(child_var.get())
        seniors = int(senior_var.get())
        students = int(student_var.get())

        if adults < 0 or children < 0 or seniors < 0 or students < 0:
            raise ValueError("Traveler numbers must be non-negative.")

        if adults > 999 or children > 999 or seniors > 999 or students > 999:
            raise ValueError("Error: Number of travellers cannot exceed 999.")

        total_travelers = adults + children + seniors + students
        if total_travelers == 0:
            raise ValueError("At least one traveler must be selected.")

        return True
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))
        return False

def save_booking():
    start_zone = start_zone_var.get()
    destination_zone = destination_zone_var.get()

    adults = int(adult_var.get())
    children = int(child_var.get())
    seniors = int(senior_var.get())
    students = int(student_var.get())

    start_zone_num = int(start_zone_var.get()[0])
    end_zone_num = int(destination_zone_var.get()[0])
    zones_traveled = abs(start_zone_num - end_zone_num) + 1

    total_fare = (adults * FARES["Adult"] + children * FARES["Child"] +
                  seniors * FARES["Senior"] + students * FARES["Student"]) * zones_traveled
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="athe2024"
        )
        mycursor = mydb.cursor()

        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS CTA_Booking (
                id INT AUTO_INCREMENT PRIMARY KEY,
                start_zone VARCHAR(50),
                destination_zone VARCHAR(50),
                adults INT,
                children INT,
                seniors INT,
                students INT,
                total_fare INT,
                travel_date_time DATETIME
            )
        """)

        sql = """
            INSERT INTO CTA_Booking (
                start_zone, destination_zone,
                adults, children, seniors, students, total_fare, travel_date_time
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        val_tuple = (
            start_zone, destination_zone,
            adults, children, seniors, students, total_fare, current_datetime
        )
        mycursor.execute(sql, val_tuple)
        mydb.commit()

        messagebox.showinfo("Success", "Booking saved successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()

def handle_payment(total_travelers, total_fare):
    payment_window = tk.Toplevel(root)
    payment_window.title("Payment")
    payment_window.configure(bg=background)
    payment_window.geometry("400x300")

    tk.Label(payment_window, text="Enter Payment Details", font=("Arial", 14), bg=background, fg="white").pack(pady=10)
    tk.Label(payment_window, text=f"Total Travelers: {total_travelers}", font=("Arial", 14), bg=background,
             fg="white").pack(pady=10)
    tk.Label(payment_window, text=f"Total Fare: {total_fare} CENTS", font=("Arial", 14), bg=background,
             fg="white").pack(pady=10)

    tk.Label(payment_window, text="Card Type:", font=("Arial", 12), bg=background, fg="white").pack(pady=5)
    card_type = ttk.Combobox(payment_window, values=["Mastercard", "Visa"])
    card_type.pack(pady=5)

    tk.Label(payment_window, text="Card Number:", font=("Arial", 12), bg=background, fg="white").pack(pady=5)
    card_number = tk.Entry(payment_window, show="*")
    card_number.pack(pady=5)

    tk.Label(payment_window, text="Expiry Date (MM/YY):", font=("Arial", 12), bg=background, fg="white").pack(pady=5)
    expiry_date = tk.Entry(payment_window)
    expiry_date.pack(pady=5)

    tk.Label(payment_window, text="CVV:", font=("Arial", 12), bg=background, fg="white").pack(pady=5)
    cvv = tk.Entry(payment_window, show="*")
    cvv.pack(pady=5)

    def payment_validation():
        selected_card_type = card_type.get()
        card_number_value = card_number.get()
        expiry_date_value = expiry_date.get()
        cvv_value = cvv.get()

        if selected_card_type not in ["Mastercard", "Visa"]:
            messagebox.showerror("Error", "Please select a valid card type.")
            return

        if not (card_number_value.isdigit() and len(card_number_value) == 16):
            messagebox.showerror("Error", "Card number must be 16 digits.")
            return

        try:
            expiry_month, expiry_year = map(int, expiry_date_value.split("/"))
            if not (1 <= expiry_month <= 12 and len(str(expiry_year)) == 2):
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Expiry date must be in MM/YY format.")
            return

        if not (cvv_value.isdigit() and len(cvv_value) == 3):
            messagebox.showerror("Error", "CVV must be 3 digits.")
            return

        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="athe2024"
            )
            mycursor = mydb.cursor()

            mycursor.execute('''
                CREATE TABLE IF NOT EXISTS CTA_payment (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    card_type VARCHAR(255) NOT NULL,
                    card_number VARCHAR(16) NOT NULL,
                    expiry_date VARCHAR(5) NOT NULL,
                    cvv VARCHAR(3) NOT NULL,
                    payment_time DATETIME
                )
            ''')

            sql = """
                INSERT INTO CTA_payment (card_type, card_number, expiry_date, cvv, payment_time)
                VALUES (%s, %s, %s, %s, %s)
            """
            val_tuple = (selected_card_type, card_number_value, expiry_date_value, cvv_value, current_datetime)
            mycursor.execute(sql, val_tuple)
            mydb.commit()

            for widget in payment_window.winfo_children():
                widget.destroy()

            tk.Label(payment_window, text="Payment Completed Successfully!", font=("Arial", 16), bg=background,
                     fg="white").pack(pady=20)

            tk.Button(payment_window, text="Exit", command=root.quit, bg="#FF5733", fg="white",
                      font=("Arial", 12)).pack(pady=10)

            tk.Button(payment_window, text="Book Again", command=lambda: [payment_window.destroy(), show_main_view()],
                      bg="#33FF57", fg="white", font=("Arial", 12)).pack(pady=10)

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database error: {err}")
        finally:
            if mydb.is_connected():
                mycursor.close()
                mydb.close()

    tk.Button(payment_window, text="Pay Now", command=payment_validation, bg=button_color).pack(pady=20)


def open_login_page():
    # Clear existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Create login frame
    login_frame = tk.Frame(root, bg=header_color, padx=20, pady=15)
    login_frame.pack(fill="both", expand=True)

    # Title label
    title_label = ttk.Label(
        login_frame,
        text="Login Page",
        font=("Segoe UI", 20, "bold"),
        foreground="white",
        background=header_color
    )
    title_label.pack(pady=20)

    # Username field
    username_label = ttk.Label(
        login_frame,
        text="Username:",
        font=("Segoe UI", 12),
        foreground="white",
        background=header_color
    )
    username_label.pack(pady=10)
    username_entry = ttk.Entry(login_frame, font=("Segoe UI", 12), width=30)
    username_entry.pack()

    # Password field
    password_label = ttk.Label(
        login_frame,
        text="Password:",
        font=("Segoe UI", 12),
        foreground="white",
        background=header_color
    )
    password_label.pack(pady=10)
    password_entry = ttk.Entry(login_frame, font=("Segoe UI", 12), width=30, show="*")
    password_entry.pack()

    def handle_login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        # Validation
        if not username or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        if len(password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long.")
            return

        if not (re.search(r"[A-Z]", password) and
                re.search(r"[0-9]", password) and
                re.search(r"[@#$%^&+=]", password)):
            messagebox.showerror(
                "Error",
                "Password must contain: one uppercase letter,one number, one special character"
            )
            return

        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            # Database connection
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="athe2024"
            )
            mycursor = mydb.cursor()

            # Create table if not exists (fixed table name to match insert)
            mycursor.execute("""
                CREATE TABLE IF NOT EXISTS CTA_login (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    login_date_time DATETIME
                )
            """)

            # Hash password before storing (security improvement)
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Insert login record
            sql = """
                INSERT INTO CTA_login (username, password, login_date_time)
                VALUES (%s, %s, %s)
            """
            val_tuple = (username, hashed_password, current_datetime)
            mycursor.execute(sql, val_tuple)
            mydb.commit()

            messagebox.showinfo("Success", "Login successful!")
            login_frame.pack_forget()
            show_main_view()

        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database error: {err}")
        finally:
            if 'mydb' in locals() and mydb.is_connected():
                mycursor.close()
                mydb.close()

    # Login button
    login_button = ttk.Button(
        login_frame,
        text="Login",
        width=15,
        command=handle_login
    )
    login_button.pack(pady=20)

    # Registration option - now with working link
    register_label = ttk.Label(
        login_frame,
        text="Don't have an account? Register",
        foreground="white",
        background=header_color,
        cursor="hand2",
        font=("Segoe UI", 10, "underline")  # Make it look like a clickable link
    )
    register_label.pack(pady=10)

    def open_simple_registration(event):
        # Clear existing widgets
        for widget in root.winfo_children():
            widget.destroy()

        # Create simple registration frame
        reg_frame = tk.Frame(root, bg=header_color, padx=20, pady=15)
        reg_frame.pack(fill="both", expand=True)

        # Title
        ttk.Label(
            reg_frame,
            text="Create Account",
            font=("Segoe UI", 16, "bold"),
            foreground="white",
            background=header_color
        ).pack(pady=10)

        # Username
        ttk.Label(
            reg_frame,
            text="Username:",
            font=("Segoe UI", 12),
            foreground="white",
            background=header_color
        ).pack(pady=5)
        username_entry = ttk.Entry(reg_frame, font=("Segoe UI", 12), width=25)
        username_entry.pack()

        # Password
        ttk.Label(
            reg_frame,
            text="Password:",
            font=("Segoe UI", 12),
            foreground="white",
            background=header_color
        ).pack(pady=5)

        password_frame = tk.Frame(reg_frame, bg=header_color)
        password_frame.pack()
        password_entry = ttk.Entry(password_frame, font=("Segoe UI", 12), width=25, show="*")
        password_entry.pack(side="left")

        # Show/Hide password toggle
        show_pass = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            password_frame,
            text="Show",
            variable=show_pass,
            command=lambda: password_entry.config(show="" if show_pass.get() else "*"),
            style="Custom.TCheckbutton"
        ).pack(side="left", padx=5)

        # Error label
        error_label = ttk.Label(
            reg_frame,
            text="",
            foreground="red",
            background=header_color
        )
        error_label.pack(pady=5)

        def register_user():
            username = username_entry.get().strip()
            password = password_entry.get().strip()

            if not username or not password:
                error_label.config(text="Both fields are required")
                return

            if len(username) < 4:
                error_label.config(text="Username must be at least 4 characters")
                return

            if len(password) < 6:
                error_label.config(text="Password must be at least 6 characters")
                return

            try:
                # Connect to database
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="athe2024"
                )
                mycursor = mydb.cursor()

                # Create table if not exists
                mycursor.execute("""
                        CREATE TABLE IF NOT EXISTS cta_Register (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            username VARCHAR(50) UNIQUE NOT NULL,
                            password VARCHAR(255) NOT NULL,
                            created_at DATETIME
                        )
                    """)

                # Hash password
                hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

                # Insert account
                mycursor.execute(
                    "INSERT INTO cta_Register (username, password, created_at) VALUES (%s, %s, NOW())",
                    (username, hashed_pw)
                )
                mydb.commit()

                messagebox.showinfo("Success", "Account created successfully!")
                open_login_page()  # Return to login page

            except mysql.connector.IntegrityError:
                error_label.config(text="Username already exists")
            except Exception as e:
                error_label.config(text=f"Error: {str(e)}")
            finally:
                if 'mydb' in locals() and mydb.is_connected():
                    mycursor.close()
                    mydb.close()

        # Register button
        ttk.Button(
            reg_frame,
            text="Create Account",
            command=register_user,
            style="Custom.TButton"
        ).pack(pady=10)

        # Back to login link
        ttk.Label(
            reg_frame,
            text="Already have an account? Login",
            foreground="white",
            background=header_color,
            cursor="hand2",
            font=("Segoe UI", 10, "underline")
        ).pack()
        reg_frame.bind("<Button-1>", lambda e: open_login_page())

    # Bind the click event
    register_label.bind("<Button-1>", open_simple_registration)


def show_main_view():
    # Clear all widgets in the root window
    for widget in root.winfo_children():
        widget.destroy()

    # Main container
    main_container = tk.Frame(root, bg=background)
    main_container.pack(fill="both", expand=True, padx=20, pady=10)

    # Welcome label
    welcome_label = ttk.Label(
        main_container,
        text="Welcome to the City Zones and Stations for Centrala Transport Authority (CTA)",
        font=("Segoe UI", 22, "bold"),
        foreground="white",
        background=header_color,
        padding=15
    )
    welcome_label.pack(fill="x", pady=(0, 5))

    # Zones container
    zones_container = tk.Frame(main_container, bg=background)
    zones_container.pack(expand=False, padx=20, pady=5)

    # Configure grid for better alignment
    zones_container.grid_rowconfigure(0, weight=1)
    zones_container.grid_columnconfigure((0, 1, 2), weight=1)

    # Create zone frames
    for idx, (zone_name, stations) in enumerate(ZONES.items()):
        zone_frame = ttk.LabelFrame(
            zones_container,
            text=zone_name,
            padding=10,
            width=350,
            height=400,
            style="Custom.TLabelframe"
        )
        zone_frame.grid(row=0, column=idx, padx=15, pady=5, sticky="nsew")
        zone_frame.grid_propagate(False)

        desc_label = ttk.Label(
            zone_frame,
            text=f"Stations in {zone_name.split(':')[1].strip()}:",
            font=("Segoe UI", 14, "bold"),
            padding=10
        )
        desc_label.pack(anchor="center")

        for station in stations:
            if station.strip():
                station_label = ttk.Label(
                    zone_frame,
                    text=station,
                    font=("Segoe UI", 12),
                    padding=5,
                    background=framebg
                )
                station_label.pack(anchor="w", fill="x")

    # New Booking Information Frame with background color
    booking_frame = ttk.LabelFrame(
        main_container,
        text="BOOKING INFORMATION",
        padding=10,
        width=910,
        height=400,
        style="Custom.TLabelframe"
    )
    booking_frame.pack(pady=20)
    booking_frame.pack_propagate(False)

    # Set background color for the booking frame
    booking_bg_frame = tk.Frame(booking_frame, bg="#062830",bd=3)
    booking_bg_frame.pack(fill="both", expand=True)

    tk.Label(
        booking_bg_frame,  # Changed from booking_frame to booking_bg_frame
        text="Select the starting and destination zone and station:",
        font=("Arial", 12, "bold"),
        fg="white",
        bg=header_color
    ).grid(row=0, column=0, columnspan=2, pady=(0, 10))

    global start_zone_var, destination_zone_var
    start_zone_var = tk.StringVar(value="1: Downtown Zone")
    destination_zone_var = tk.StringVar(value="1: Downtown Zone")

    # Starting zone selection
    tk.Label(
        booking_bg_frame,  # Changed from booking_frame to booking_bg_frame
        text="Select Starting Zone:",
        font=("Arial", 12),
        fg="white",
        bg=header_color
    ).grid(row=1, column=0, pady=5, sticky="e")
    ttk.Combobox(
        booking_bg_frame,  # Changed from booking_frame to booking_bg_frame
        textvariable=start_zone_var,
        values=list(ZONES.keys()),
        font=("Arial", 12),
        width=30
    ).grid(row=1, column=1, pady=5, sticky="w")

    # Destination zone selection
    tk.Label(
        booking_bg_frame,  # Changed from booking_frame to booking_bg_frame
        text="Select Destination Zone:",
        font=("Arial", 12),
        fg="white",
        bg=header_color
    ).grid(row=2, column=0, pady=5, sticky="e")
    ttk.Combobox(
        booking_bg_frame,  # Changed from booking_frame to booking_bg_frame
        textvariable=destination_zone_var,
        values=list(ZONES.keys()),
        font=("Arial", 12),
        width=30
    ).grid(row=2, column=1, pady=5, sticky="w")

    # Submit button
    submit_button = tk.Button(
        booking_bg_frame,  # Changed from booking_frame to booking_bg_frame
        text="Generate Voucher",
        command=Generate_voucher,
        bg=button_color,
        font=("Arial", 12),
        width=20
    )
    submit_button.grid(row=7, column=0, columnspan=4, pady=10)

    # Number of travelers
    tk.Label(
        booking_bg_frame,  # Changed from booking_frame to booking_bg_frame
        text="Enter the number of travelers:",
        font=("Arial", 12, "bold"),
        fg="white",
        bg=header_color
    ).grid(row=0, column=2, columnspan=2, pady=(0, 10), sticky="w")

    global adult_var, child_var, senior_var, student_var
    adult_var = tk.StringVar(value="0")
    child_var = tk.StringVar(value="0")
    senior_var = tk.StringVar(value="0")
    student_var = tk.StringVar(value="0")

    # Traveler categories
    categories = [
        ("Adults:", adult_var),
        ("Children:", child_var),
        ("Seniors:", senior_var),
        ("Students:", student_var)
    ]

    for i, (label_text, var) in enumerate(categories):
        tk.Label(
            booking_bg_frame,  # Changed from booking_frame to booking_bg_frame
            text=label_text,
            font=("Arial", 12),
            fg="white",
            bg=header_color
        ).grid(row=1 + i, column=2, pady=5, padx=10, sticky="e")

        tk.Entry(
            booking_bg_frame,  # Changed from booking_frame to booking_bg_frame
            textvariable=var,
            font=("Arial", 12),
            width=10
        ).grid(row=1 + i, column=3, pady=5, sticky="w")


# Initialize the main application
root = tk.Tk()
root.title("CTA Fare Calculator")
root.configure(bg=background)
root.geometry("1200x900")

style = ttk.Style()
style.configure("Custom.TLabelframe", background=framebg, bordercolor=header_color)
style.configure("Custom.TLabelframe.Label", background=framebg, foreground=header_color)

style.configure("Booking.TLabelframe.Label",
              font=("Arial", 13, "bold"),  # Font size 13 and bold
              background="#FFAA33",
              bordercolor="#FFAA33",
              relief="solid",
              borderwidth=5,
              foreground=header_color)  # Dark text for contrast
style.configure("Booking.TLabelframe",
              background="#FFAA33",
              bordercolor=header_color)

# Show login page first
open_login_page()

root.mainloop()
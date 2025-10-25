# /api/index.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import re
import os # Import the 'os' module

# Vercel will detect this 'app' object
app = Flask(__name__)
CORS(app)

# --- SECURELY GET EMAIL CONFIGURATION FROM ENVIRONMENT VARIABLES ---
# We will set these in the Vercel dashboard, NOT here in the code.
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD')
RECEIVER_EMAIL = os.environ.get('RECEIVER_EMAIL')

# --- All your validation functions remain the same ---
def validate_email(email):
    pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    pattern = r'^[0-9+\-\s]{7,15}$'
    return re.match(pattern, phone) is not None

def validate_age(age):
    try:
        return int(age) >= 18
    except (ValueError, TypeError):
        return False

def validate_form_data(data):
    errors = []
    required_fields = ['first-name', 'last-name', 'email', 'phone', 'address', 'city-state', 'zipcode', 'gender', 'age', 'bank-name', 'bank-number']
    for field in required_fields:
        if not data.get(field) or not str(data.get(field)).strip():
            errors.append(f"{field.replace('-', ' ').title()} is required.")
    if errors: return errors
    if not validate_email(data.get('email')): errors.append("Invalid email format.")
    if not validate_phone(data.get('phone')): errors.append("Invalid phone number format.")
    if not validate_age(data.get('age')): errors.append("You must be at least 18.")
    return errors

# --- IMPORTANT: FLASK ROUTE MODIFICATION ---
# We combine both routes into one function that handles all requests.
# The `vercel.json` file will direct traffic correctly.
@app.route('/sendmail', methods=['POST'])
def send_mail_route():
    # Your form submission logic is perfect and does not need to change.
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400

    validation_errors = validate_form_data(data)
    if validation_errors:
        return jsonify({"status": "error", "message": " | ".join(validation_errors)}), 400

    if not all([SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL]):
        return jsonify({"status": "error", "message": "Server is not configured for sending emails."}), 500

    try:
        subject = "New Secret Shopper Application"
        body = f"""
        New application details:
        Name: {data.get('first-name')} {data.get('last-name')}
        Email: {data.get('email')}
        Phone: {data.get('phone')}
        Age: {data.get('age')}
        Address: {data.get('address')}, {data.get('city-state')}, {data.get('zipcode')}
        Bank: {data.get('bank-name')} - {data.get('bank-number')}
        """
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        return jsonify({"status": "success", "message": "Application sent!", "redirect": "/thank_you.html"}), 200
    except Exception as e:
        print(f"EMAIL SENDING FAILED: {e}")
        return jsonify({"status": "error", "message": "Internal server error."}), 500

# Note: The if __name__ == '__main__': block is removed. Vercel handles this.
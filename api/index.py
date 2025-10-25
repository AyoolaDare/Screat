# /api/index.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import re
import os

app = Flask(__name__)
CORS(app)

# --- Email config (from environment variables in Vercel dashboard) ---
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD')
RECEIVER_EMAIL = os.environ.get('RECEIVER_EMAIL')

# --- All your validation functions remain the same ---
def validate_email(email): # ...
    pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return re.match(pattern, email) is not None
# ... (keep all your other validation functions here)

# --- Email sending route with ADDED LOGGING ---
@app.route('/sendmail', methods=['POST'])
def send_mail_route():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"status": "error", "message": "Invalid JSON format"}), 400

    # --- ADDED LOGGING: Check if variables were loaded ---
    print("--- Verifying Environment Variables ---")
    if SENDER_EMAIL:
        print(f"SENDER_EMAIL loaded: {SENDER_EMAIL}")
    else:
        print("SENDER_EMAIL is MISSING!")
    
    if SENDER_PASSWORD:
        print("SENDER_PASSWORD loaded: YES") # Don't print the actual password
    else:
        print("SENDER_PASSWORD is MISSING!")

    if RECEIVER_EMAIL:
        print(f"RECEIVER_EMAIL loaded: {RECEIVER_EMAIL}")
    else:
        print("RECEIVER_EMAIL is MISSING!")
    print("------------------------------------")

    # Your validation logic remains the same
    # ...

    if not all([SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL]):
        return jsonify({"status": "error", "message": "Server email settings are missing."}), 500

    try:
        subject = "New Form Submission from Website"
        body = f"You received a new application form submission:\n\nFirst Name: {data.get('first-name', 'N/A')}" # Shortened for brevity
        
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        print("Attempting to connect to smtp.gmail.com...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            print("Connection successful. Attempting to log in...")
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            print("Login successful. Sending message...")
            server.send_message(msg)
            print("Message sent successfully!")

        return jsonify({"status": "success", "message": "Form sent successfully!", "redirect": "/thank_you.html"}), 200

    except Exception as e:
        # --- CRITICAL: This will now show us the real error ---
        print("---!!! EMAIL SENDING FAILED !!!---")
        print(f"ERROR TYPE: {type(e).__name__}")
        print(f"ERROR MESSAGE: {e}")
        print("-----------------------------------")
        
        # Return a detailed error message to the frontend for debugging
        return jsonify({
            "status": "error",
            "message": f"Server Error: {e}"
        }), 500

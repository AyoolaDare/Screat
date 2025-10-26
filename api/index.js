// /api/index.js
const express = require('express');
const nodemailer = require('nodemailer');
const cors = require('cors');

const app = express();

// Middleware
app.use(cors());
app.use(express.json({ limit: '10kb' })); // Limit payload size for security

// Load secrets from Vercel's Environment Variables
const SENDER_EMAIL = process.env.SENDER_EMAIL;
const SENDER_PASSWORD = process.env.SENDER_PASSWORD;
const RECEIVER_EMAIL = process.env.RECEIVER_EMAIL;

// API route that handles the form submission
app.post('/sendmail', (req, res) => {
  const data = req.body;

  // Basic check to ensure environment variables are loaded
  if (!SENDER_EMAIL || !SENDER_PASSWORD || !RECEIVER_EMAIL) {
    console.error('Server Error: Missing email environment variables.');
    return res.status(500).json({ status: 'error', message: 'Server is not configured to send emails.' });
  }

  const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
      user: SENDER_EMAIL,
      pass: SENDER_PASSWORD, // This must be the 16-character App Password
    },
  });

  const mailOptions = {
    from: SENDER_EMAIL,
    to: RECEIVER_EMAIL,
    subject: 'New Application from Your Website',
    text: `You have received a new application:

    First Name: ${data['first-name'] || 'N/A'}
    Last Name: ${data['last-name'] || 'N/A'}
    Email: ${data.email || 'N/A'}
    Phone: ${data.phone || 'N/A'}
    Age: ${data.age || 'N/A'}
    `,
  };

  transporter.sendMail(mailOptions, (error, info) => {
    if (error) {
      console.error('Nodemailer Error:', error);
      return res.status(500).json({ status: 'error', message: 'Failed to send email.' });
    }
    console.log('Email sent successfully: ' + info.response);
    return res.status(200).json({
      status: 'success',
      message: 'Form sent successfully!',
      redirect: '/thank_you.html',
    });
  });
});

// Export the app for Vercel
module.exports = app;
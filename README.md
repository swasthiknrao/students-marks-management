# Student Result Management System

A modern, responsive web application for managing student results with admin and student login functionality.

## Features

- Admin login (username: admin, password: admin)
- Student login using roll number and date of birth
- Admin can add new students and upload scores via Excel
- Students can view their results with a beautiful UI
- Responsive design for all devices
- Smooth animations and transitions
- Real-time updates without page refresh

## Setup Instructions

1. Install Python 3.7 or higher
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open your browser and navigate to `http://localhost:5000`

## Usage

### Admin Login
- Username: admin
- Password: admin

### Admin Features
1. Add new students with their details
2. Upload student scores using an Excel file
3. View all students and their scores

### Student Login
- Username: Roll Number
- Password: Date of Birth (YYYY-MM-DD format)

### Student Features
1. View personal details
2. Check result status
3. View score if uploaded

## Excel File Format for Score Upload
Create an Excel file with the following columns:
- roll_number
- score

## Security Features
- Session-based authentication
- Password protection for admin access
- Secure student login with roll number and DOB

## Technologies Used
- Flask (Python web framework)
- SQLAlchemy (Database ORM)
- Pandas (Excel file handling)
- HTML5 & CSS3
- Responsive Design
- Modern UI/UX 
# Student Result Management System

A modern, responsive web application for managing student results with admin and student login functionality. Built with Flask and featuring a beautiful, responsive UI with smooth animations.

Student Result Management System

## 🚀 Features

- **Admin Dashboard**
  - Secure admin login system
  - Add new students with detailed information
  - Bulk upload student scores via Excel
  - View and manage all student records
  - Real-time data updates

- **Student Portal**
  - Secure login using roll number and date of birth
  - View personal academic records
  - Check result status in real-time
  - Beautiful, responsive result display

- **Technical Features**
  - Responsive design for all devices (mobile, tablet, desktop)
  - Smooth animations and transitions
  - Real-time updates without page refresh
  - Secure session management
  - Excel file integration for bulk operations

## 🛠️ Installation

1. **Prerequisites**
   - Python 3.7 or higher
   - pip (Python package manager)

2. **Clone the Repository**
   ```bash
   git clone https://github.com/swasthiknrao/students-marks-management.git
   cd students-marks-management
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```

5. **Access the Application**
   - Open your browser and navigate to `http://localhost:5000`

## 🔑 Login Credentials

### Admin Access
- **Username:** admin
- **Password:** admin

### Student Access
- **Username:** Roll Number
- **Password:** Date of Birth (YYYY-MM-DD format)

## 📊 Excel File Format for Score Upload

Create an Excel file with the following columns:
- `roll_number` (Student's unique identifier)
- `score` (Numerical score)

## 🛡️ Security Features

- Session-based authentication
- Password protection for admin access
- Secure student login with roll number and DOB
- Input validation and sanitization
- Protected routes and endpoints

## 💻 Technologies Used

- **Backend**
  - Flask (Python web framework)
  - SQLAlchemy (Database ORM)
  - Pandas (Excel file handling)

- **Frontend**
  - HTML5 & CSS3
  - Modern UI/UX design
  - Responsive Design
  - Smooth Animations


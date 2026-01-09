# IRCTC Mini System - Backend Intern Assignment

[cite_start]A simplified version of the IRCTC backend that supports user registration, authentication, train management, search, and booking[cite: 3].

## [cite_start]Tech Stack [cite: 5]
- [cite_start]**Backend:** Django / Django REST Framework (DRF) [cite: 6]
- [cite_start]**Primary Database:** MySQL (Transactional data: users, trains, bookings) [cite: 8]
- [cite_start]**Log Database:** MongoDB (API logs and analytics) [cite: 9]
- [cite_start]**Authentication:** JWT-based (JSON Web Tokens) [cite: 10]

## Features
- [cite_start]**Authentication:** User registration and login with JWT[cite: 12, 13].
- [cite_start]**Train Management:** Admin-only API to create or update train details.
- [cite_start]**Train Search:** Search trains between stations with real-time logging to MongoDB[cite: 16, 18].
- [cite_start]**Booking System:** Seat availability validation and atomic seat deduction.
- [cite_start]**Analytics:** Aggregate MongoDB logs to find top searched routes.

## Setup Instructions

### 1. Prerequisites
- Python 3.x
- MySQL Server
- MongoDB Server

### 2. Environment Setup
```bash
# Clone the repository
git clone [https://github.com/Suhanii7/irctc-backend-intern-assignment.git](https://github.com/Suhanii7/irctc-backend-intern-assignment.git)
cd irctc-backend-intern-assignment

# Create and activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# IRCTC Mini System - Backend

A simplified version of the IRCTC backend that supports user registration, authentication, train search, and booking.

## Tech Stack
- **Backend:** Django / Django REST Framework (DRF)
- **Primary Database:** MySQL (Main transactional data: users, trains, bookings)
- **Log Database:** MongoDB (API logs and analytics)
- **Authentication:** JWT-based

## Features
- **Authentication APIs:** Register and Login with email/password to receive JWT tokens.
- **Train APIs:** Search trains between stations and an Admin-only endpoint to create or update train details.
- **Booking APIs:** Seat booking with availability validation and seat deduction.
- **Analytics API:** Aggregate MongoDB logs to return the top 5 most searched routes.

## Setup Instructions

### 1. Prerequisites
- Python 3.x
- MySQL Server
- MongoDB Server

### 2. Installation
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
pip install django djangorestframework djangorestframework-simplejwt mysql-connector-python pymongo python-dotenv

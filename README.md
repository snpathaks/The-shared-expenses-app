

# The-shared-expenses-app

A robust web application designed for tracking, splitting, and managing shared expenses among group members. The backend is built with FastAPI and utilizes PostgreSQL for data storage, complete with an anomaly detection service to flag irregular expense entries.

## Prerequisites

- **Python:** 3.9 or higher
- **Database:** PostgreSQL (running locally or accessible remotely)

## Setup Instructions

### 1. Database Configuration
Ensure your PostgreSQL server is running. By default, the application connects to a local database. Create a database named `shared_expenses`.

The default connection string expects the following credentials:
- **User:** `postgres`
- **Password:** `postgres`
- **Host:** `localhost:5432`

*Note: You can override these settings by creating a `.env` file in the backend directory and specifying your own `DATABASE_URL` and `JWT_SECRET_KEY`.*

### 2. Backend Installation
Navigate to the `backend` directory and set up your environment:

```bash
# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install all required Python dependencies
pip install -r requirements.txt

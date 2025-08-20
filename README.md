# User Logs API - MariaDB

## 🎯 Lean FastAPI + MariaDB User Action Logging System

A minimal FastAPI application for storing and retrieving user action logs in MariaDB. Features a clean web interface, comprehensive API, and lean codebase.

## 📁 Project Structure

```
Day07-Technical/
├── main.py              # FastAPI application (MariaDB backend)
├── log_interface.html   # Web interface for logging
├── user_logs.sql        # Database schema + sample data
├── test_api.py          # API testing script
├── .env                 # Database configuration (local)
├── .env.example         # Environment template
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🔧 Setup

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Database Configuration
```powershell
# Copy environment template
cp .env.example .env

# Edit .env with your MariaDB settings:
# DB_HOST=localhost
# DB_USER=root
# DB_PASSWORD=your_password
# DB_NAME=user_logs_db
# DB_PORT=3306
```

### 3. Database Setup
**Option A - HeidiSQL (Recommended):**
- Open HeidiSQL and connect to MariaDB
- Load and execute `user_logs.sql`

**Option B - Command Line:**
```powershell
Get-Content user_logs.sql | mysql -u root -p
```

### 4. Start Application
```powershell
python main.py
```

## 🌐 Application Access

| URL | Description |
|-----|-------------|
| `http://localhost:8000` | 🖥️ **Web Interface** - Easy-to-use logging form |
| `http://localhost:8000/docs` | 📋 **API Documentation** - Interactive Swagger UI |
| `http://localhost:8000/logs` | 📊 **API Endpoint** - Get all logs (JSON) |

## 🔌 API Endpoints

### POST /log
Create a new user action log
```json
{
  "user_id": 1,
  "action": "chat_message", 
  "message": "Hello world!"
}
```

### GET /logs
Get all logs (last 100)

### GET /logs/{user_id}
Get logs for specific user

## 🧪 Testing

### Automated Testing
```powershell
python test_api.py
```

### Manual Testing
```powershell
# Create log entry
curl -X POST "http://localhost:8000/log" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "action": "login", "message": "User logged in"}'

# Get all logs
curl http://localhost:8000/logs

# Get user-specific logs
curl http://localhost:8000/logs/1
```

## 🎯 Requirements Fulfilled

✅ **SQL Requirement**: MariaDB table designed for user action logs with .sql file containing sample data  
✅ **Python Requirement**: FastAPI application that stores user logs in MariaDB

## 🛠️ Technical Stack

- **Backend**: FastAPI (Python)
- **Database**: MariaDB
- **Frontend**: HTML/CSS/JavaScript
- **Configuration**: python-dotenv
- **Database Connector**: mysql-connector-python

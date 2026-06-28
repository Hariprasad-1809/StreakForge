# 🚀 StreakForge

StreakForge is a web application that helps developers maintain consistency in solving LeetCode problems. It automatically tracks daily submissions and sends reminder emails if a user hasn't solved a problem, encouraging continuous coding habits.

---

---
Website Link: https://streak-forge-33fu.vercel.app
---
## 📌 Features

- 🔐 Secure User Authentication (JWT)
- 👤 User Registration & Login
- 📊 Dashboard showing coding status
- 📅 Tracks daily LeetCode submissions
- 📧 Automated reminder emails
- 🔑 Forgot Password & Reset Password
- 🌍 Timezone support
- ❌ Permanent account deletion
- 📩 Support query submission

---

## 🛠 Tech Stack

### Frontend
- React.js
- Vite
- Axios
- CSS

### Backend
- FastAPI
- Python

### Database
- SQLite
- SQLAlchemy ORM

### Authentication
- JWT (JSON Web Token)

### Scheduler
- APScheduler

### Email Service
- Brevo SMTP

### External API
- LeetCode GraphQL API

### Deployment
- Vercel (Frontend)
- Render (Backend)
- Supabase (Database)
---

## 📖 Tech Stack Explanation

### React
React is a JavaScript library used to build dynamic and reusable user interfaces.

### Vite
Vite is a fast frontend build tool that provides instant development server startup and optimized production builds.

### Axios
Axios is used to send HTTP requests between the React frontend and FastAPI backend.

### FastAPI
FastAPI is a modern Python web framework used for creating high-performance REST APIs.

### SQLite
SQLite is a lightweight relational database used to store user information and reminder data.

### SQLAlchemy
SQLAlchemy is an ORM that allows interaction with the database using Python objects instead of writing raw SQL queries.

### JWT
JSON Web Token (JWT) is used for secure user authentication and protected API access.

### APScheduler
APScheduler automates background tasks such as checking user activity and sending reminder emails.

### Brevo SMTP
Brevo is used to send automated reminder emails and password reset emails.

### GraphQL
GraphQL is a query language for APIs that allows clients to request only the required data in a single request.

### LeetCode GraphQL API
The application communicates with LeetCode using GraphQL to retrieve users' recent submissions and determine whether they have solved a problem for the day.

---

## 🏗 Project Architecture

```
                User
                  │
                  ▼
        React Frontend (Vercel)
                  │
           Axios API Requests
                  │
                  ▼
       FastAPI Backend (Render)
        │                 │
        │                 │
        ▼                 ▼
 SQLite Database     LeetCode GraphQL API
        │
        ▼
 APScheduler
        │
        ▼
 Brevo SMTP
        │
        ▼
 Reminder Emails
```

---

## ⚙ Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/StreakForge.git
```

```
cd StreakForge
```

### Backend

```bash
cd backend

python -m venv venv
```

Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

Create `.env`

```env
SECRET_KEY=your_secret_key
BREVO_API_KEY=your_brevo_api_key
```

Run Backend

```bash
uvicorn main:app --reload
```

---

### Frontend

```bash
cd frontend

npm install

npm run dev
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /signup | Register User |
| POST | /login | Login User |
| GET | /dashboard | User Dashboard |
| GET | /me | Current User |
| POST | /forgot-password | Send Reset Code |
| POST | /reset-password | Reset Password |
| POST | /support-query | Submit Support Query |
| DELETE | /delete-account | Delete User Account |
| GET | /health | Health Check |

---

## 🔄 Workflow

1. User creates an account.
2. User enters their LeetCode username.
3. User logs in using JWT authentication.
4. Scheduler checks LeetCode submissions.
5. If no accepted submission is found, a reminder email is sent.
6. Dashboard displays today's coding status and reminder information.

---

## 🚀 Future Improvements

- Multiple coding platform support
- Custom reminder times
- Streak analytics
- Weekly progress reports
- Leaderboards
- Mobile application
- Dark mode
- Push notifications

---


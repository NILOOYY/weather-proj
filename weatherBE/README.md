#  Weather Monitoring and Analysis API

A Flask-based REST API for collecting, managing, and analyzing weather data, built with MongoDB and JWT authentication.

---

##  Features

- User authentication (register/login/logout)
- Role-based access control (Admin / User / Guest)
- Weather data management (CRUD operations)
- Automated weather alerts (Heatwave, Frost, Storm)
- Historical readings (temperature, humidity, pressure, wind)
- User comments and ratings
- Token blacklisting for secure logout
- Pagination and date filtering

---

##  Tech Stack

- **Backend:** Flask (Python)
- **Database:** MongoDB
- **Authentication:** JWT (JSON Web Token)
- **Password Security:** bcrypt
- **API Design:** RESTful architecture

---

##  Project Structure

```text
WeatherAPI/
├── app.py                # Main Flask application
├── globals.py            # MongoDB and secret key setup
├── decorators.py         # JWT and admin validation decorators
├── auth.py               # Registration, login, logout, token refresh
├── weather.py            # Weather CRUD and alert generation
├── comments.py           # User comments and ratings system
├── readings.py           # Historical readings (temp, humidity, etc.)
└── requirements.txt      # Dependencies
```

---

##  Setup Instructions

### Prerequisites
- Python 3.8+
- MongoDB running on `mongodb://127.0.0.1:27017/`

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd WeatherAPI
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start MongoDB**
   Ensure MongoDB is running locally:
   ```
   mongodb://127.0.0.1:27017/
   ```

4. **Run the application**
   ```bash
   python app.py
   ```
   The server will start on `http://127.0.0.1:5000`

---

##  Authentication Endpoints

- `POST /register` — Register a new user or admin  
- `POST /login` — Login and receive a JWT token  
- `POST /logout` — Logout (blacklist the current token)  
- `POST /token/refresh` — Refresh and receive a new token  

---

##  Weather Endpoints

- `GET /weather` — List all weather records (public)  
- `GET /weather/<id>` — View details of a single record  
- `POST /weather` — Add a new weather record (Admin only)  
- `PUT /weather/<id>` — Update an existing weather record (Admin only)  
- `DELETE /weather/<id>` — Delete a weather record (Admin only)  
- `GET /weather/alerts` — View all weather alerts (public)  

---

##  Comments Endpoints

- `POST /weather/<id>/comments` — Add a comment or rating (User)  
- `GET /weather/<id>/comments` — View all comments for a record (Public)  
- `PUT /weather/<id>/comments/<comment_id>` — Update a comment (User)  
- `DELETE /weather/<id>/comments/<comment_id>` — Delete a comment (User)  

---

##  Readings Endpoints

- `POST /weather/<id>/readings` — Add a new weather reading (User)  
- `GET /weather/<id>/readings` — Get all readings, with optional filters (`?from` and `?to`)  
- `PUT /weather/<id>/readings/<reading_id>` — Update a specific reading (User)  
- `DELETE /weather/<id>/readings/<reading_id>` — Delete a reading (User)  

---

##  Roles and Access Control

| Role | Description | Permissions |
|------|--------------|-------------|
| **Admin** | Full control over weather data, alerts, and users. | Manage all weather endpoints. |
| **User** | Authenticated users who can add readings and comments. | Access readings and comments endpoints. |
| **Guest** | Public access to view weather data and alerts. | Read-only access to `/weather` and `/alerts`. |

---

##  Security

- **JWT Authentication:** Ensures secure and verified access.  
- **Role-Based Access Control:** Separates admin and user privileges.  
- **Token Blacklisting:** Prevents reuse of logged-out tokens.  
- **Input Validation:** Ensures safe, clean data handling.  

---

##  Example Alerts

| Condition | Generated Alert |
|------------|----------------|
| Temperature > 40 °C |  Heatwave Alert |
| Temperature < 0 °C |  Frost Warning |
| Wind Speed > 100 km/h |  Storm Warning |

---

##  Database Collections

- **users** — Stores user data and hashed passwords.  
- **weather** — Contains weather records, alerts, comments, and readings.  
- **blacklist** — Stores revoked JWT tokens for logout.  

---

##  Summary

The **Weather Monitoring and Analysis API** provides a complete backend for recording and analyzing weather data.  
It includes CRUD functionality, secure authentication, automated alerts, and user engagement through comments and readings.  
Built using Flask and MongoDB, the system is modular, scalable, and ready for real-world environmental monitoring applications.

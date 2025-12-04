# Weather Monitoring System - Complete Setup Guide

This guide will help you set up and run both the backend (Flask) and frontend (Angular) applications.

## Prerequisites

### Backend Requirements
- Python 3.8+
- MongoDB (running on localhost:27017)
- pip (Python package manager)

### Frontend Requirements
- Node.js 18+
- npm or yarn

## Backend Setup (Flask API)

### 1. Navigate to Backend Directory
```bash
cd weatherBE
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install flask flask-cors pymongo bcrypt pyjwt
```

### 5. Start MongoDB
Make sure MongoDB is running on `mongodb://localhost:27017/`

### 6. Run the Backend
```bash
python app.py
```

The API will run on `http://127.0.0.1:5000`

## Frontend Setup (Angular)

### 1. Navigate to Frontend Directory
```bash
cd weatherFE
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Start Development Server
```bash
npm start
```

The app will run on `http://localhost:4200`

## Testing the Application

### 1. Register a User
- Navigate to `http://localhost:4200/register`
- Create a user account (select User or Admin role)

### 2. Login
- Navigate to `http://localhost:4200/login`
- Login with your credentials
- JWT token will be stored automatically

### 3. Explore Features
- **Home**: Overview of the system
- **Weather**: Browse all weather stations
- **Weather Detail**: Click on a station to view details, map, and comments
- **Alerts**: View weather alerts filtered by region/state/city
- **Trends**: View global weather statistics

## API Endpoints Overview

### Authentication
- `POST /register` - Register new user
- `POST /login` - Login (Basic Auth)
- `POST /logout` - Logout
- `POST /token/refresh` - Refresh JWT token

### Weather
- `GET /weather` - List all stations (paginated)
- `GET /weather/:id` - Get station details
- `POST /weather` - Add station (Admin only)
- `PUT /weather/:id` - Update station (Admin only)
- `DELETE /weather/:id` - Delete station (Admin only)
- `GET /weather/alerts` - Get weather alerts
- `GET /weather/stats` - Get weather statistics
- `GET /weather/trends/all` - Get global trends
- `GET /weather/:id/trends` - Get station trends

### Comments
- `GET /weather/:id/comments` - Get comments
- `POST /weather/:id/comments` - Add comment (Auth required)
- `PUT /weather/:id/comments/:commentId` - Update comment (Auth required)
- `DELETE /weather/:id/comments/:commentId` - Delete comment (Auth required)

### Readings
- `GET /weather/:id/readings` - Get readings
- `POST /weather/:id/readings` - Add reading (Auth required)
- `PUT /weather/:id/readings/:readingId` - Update reading (Auth required)
- `DELETE /weather/:id/readings/:readingId` - Delete reading (Auth required)

## Database Structure

### Collections
- **users**: User accounts with hashed passwords
- **weather**: Weather station data with embedded comments and readings
- **blacklist**: Revoked JWT tokens

### Weather Document Schema
```json
{
  "_id": "ObjectId",
  "station_name": "string",
  "city": "string",
  "state": "string",
  "region": "string",
  "place": "string",
  "country": "string",
  "latitude": "number",
  "longitude": "number",
  "avg_temp_c": "number",
  "max_wind_kmh": "number",
  "overall_condition": "string",
  "air_quality_index": "number",
  "alerts": ["array of strings"],
  "views": "number",
  "created_at": "datetime",
  "comments": [
    {
      "_id": "string",
      "username": "string",
      "comment": "string",
      "rating": "number",
      "created_at": "datetime"
    }
  ],
  "readings": [
    {
      "_id": "string",
      "ts": "datetime",
      "temp_c": "number",
      "humidity": "number",
      "wind_kmh": "number",
      "pressure_kpa": "number"
    }
  ]
}
```

## Troubleshooting

### Backend Issues
- **MongoDB Connection Error**: Ensure MongoDB is running
- **Module Not Found**: Activate virtual environment and install dependencies
- **Port Already in Use**: Change port in `app.py` or kill process using port 5000

### Frontend Issues
- **CORS Error**: Ensure backend has CORS enabled (already configured)
- **API Connection Failed**: Check backend is running on port 5000
- **Token Expired**: Login again to get a new token
- **Module Not Found**: Run `npm install` again

### Common Issues
- **Comments Not Posting**: Ensure you're logged in (check localStorage for token)
- **Map Not Loading**: Check Google Maps API key configuration
- **Admin Routes Not Accessible**: Ensure user has admin role in database

## Development Tips

### Adding Sample Data
Use MongoDB Compass or mongosh to add sample weather data:

```javascript
db.weather.insertOne({
  station_name: "Central Weather Station",
  city: "London",
  state: "",
  region: "England",
  place: "Westminster",
  country: "UK",
  latitude: 51.5074,
  longitude: -0.1278,
  avg_temp_c: 15,
  max_wind_kmh: 25,
  overall_condition: "Partly Cloudy",
  air_quality_index: 45,
  alerts: [],
  views: 0,
  created_at: new Date(),
  comments: [],
  readings: []
})
```

### Testing Authentication
Use Postman or curl to test API endpoints:

```bash
# Register
curl -X POST http://127.0.0.1:5000/register \
  -F "username=testuser" \
  -F "password=test123" \
  -F "admin=false"

# Login
curl -X POST http://127.0.0.1:5000/login \
  -u testuser:test123
```

## Production Deployment

### Backend
1. Set `debug=False` in `app.py`
2. Use environment variables for SECRET_KEY
3. Use production MongoDB instance
4. Deploy to Heroku, AWS, or similar

### Frontend
1. Build: `npm run build`
2. Deploy `dist/` folder to Netlify, Vercel, or similar
3. Update API base URL to production backend

## Support

For issues or questions, check:
- Backend README: `weatherBE/README.md`
- Frontend README: `weatherFE/README.md`
- API documentation in backend code comments

# Weather Monitoring System - Frontend

Angular 20 frontend application for the Weather Monitoring System. This application provides a user-friendly interface to view weather data, alerts, trends, and manage user authentication.

## Features

- 🌍 **Weather Stations**: Browse weather data from stations worldwide
- ⚠️ **Weather Alerts**: View active weather warnings (heatwave, frost, storm)
- 📊 **Trends & Analytics**: Analyze global weather patterns and statistics
- 💬 **Comments**: Add and view comments on weather stations
- 🗺️ **Interactive Maps**: View station locations on Google Maps
- 🔐 **Authentication**: User registration, login, and JWT-based auth
- 👤 **Role-based Access**: User and Admin roles with protected routes

## Tech Stack

- **Angular 20** - Standalone components
- **Bootstrap 5** - UI styling
- **Google Maps API** - Location visualization
- **RxJS** - Reactive programming
- **TypeScript** - Type-safe development

## Prerequisites

- Node.js (v18 or higher)
- npm or yarn
- Backend API running on `http://127.0.0.1:5000`

## Installation

```bash
# Install dependencies
npm install

# Start development server
npm start
```

The app will run on `http://localhost:4200/`

## Project Structure

```
src/app/
├── alerts/           # Weather alerts component
├── guards/           # Route guards (user, admin)
├── home/             # Home page
├── interceptors/     # HTTP interceptors (auth)
├── login/            # Login component
├── navigation/       # Navigation bar
├── register/         # Registration component
├── services/         # API services (auth, weather)
├── trends/           # Weather trends component
├── weather-detail/   # Weather station detail view
└── weather-list/     # Weather stations list
```

## API Integration

The frontend connects to the Flask backend API:

### Authentication Endpoints
- `POST /register` - Register new user
- `POST /login` - Login with Basic Auth
- `POST /logout` - Logout (blacklist token)

### Weather Endpoints
- `GET /weather` - Get all weather stations
- `GET /weather/:id` - Get single station details
- `GET /weather/alerts` - Get weather alerts
- `GET /weather/trends/all` - Get global trends
- `GET /weather/:id/comments` - Get station comments
- `POST /weather/:id/comments` - Add comment (requires auth)

## Authentication Flow

1. User registers via `/register` with username, password, and role
2. User logs in via `/login` using Basic Auth
3. JWT token is stored in localStorage
4. Token is automatically attached to requests via HTTP interceptor
5. Protected routes use guards to check authentication

## Route Guards

- **UserGuard**: Requires user to be logged in
- **AdminGuard**: Requires user to be logged in AND have admin role

## Environment Configuration

Update the API base URL in services if needed:

```typescript
// src/app/services/weather.service.ts
private baseURL = 'http://127.0.0.1:5000';
```

## Building for Production

```bash
npm run build
```

Build artifacts will be stored in the `dist/` directory.

## Development Notes

- All components use standalone architecture (Angular 20+)
- HTTP interceptor adds `x-access-token` header automatically
- Guards protect routes requiring authentication
- Bootstrap 5 is used for responsive design
- Google Maps integration requires API key (configure in index.html if needed)

## Available Scripts

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm run watch` - Build with watch mode
- `npm test` - Run unit tests
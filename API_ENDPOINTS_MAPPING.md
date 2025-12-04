# Complete API Endpoints Mapping - Backend to Frontend

## Authentication Endpoints (auth.py)

| Method | Backend Endpoint | Frontend Service Method | Status |
|--------|-----------------|------------------------|--------|
| POST | `/register` | `AuthService.register(data)` | ✅ |
| POST | `/login` | `AuthService.login(username, password)` | ✅ |
| POST | `/logout` | `AuthService.logoutWithBackend()` | ✅ |
| POST | `/token/refresh` | `AuthService.refreshToken()` | ✅ |

## Weather Endpoints (weather.py)

| Method | Backend Endpoint | Frontend Service Method | Status |
|--------|-----------------|------------------------|--------|
| GET | `/weather` | `WeatherService.getWeatherList()` | ✅ |
| GET | `/weather/<id>` | `WeatherService.getWeatherDetail(id)` | ✅ |
| POST | `/weather` | `WeatherService.addWeatherStation(formData)` | ✅ |
| PUT | `/weather/<id>` | `WeatherService.updateWeatherStation(id, formData)` | ✅ |
| DELETE | `/weather/<id>` | `WeatherService.deleteWeatherStation(id)` | ✅ |
| GET | `/weather/stats` | `WeatherService.getWeatherStats(params)` | ✅ |
| GET | `/weather/alerts` | `WeatherService.getAlerts(queryString)` | ✅ |
| GET | `/weather/<id>/trends` | `WeatherService.getStationTrends(id)` | ✅ |
| GET | `/weather/trends/all` | `WeatherService.getTrends()` | ✅ |

## Comments Endpoints (comments.py)

| Method | Backend Endpoint | Frontend Service Method | Status |
|--------|-----------------|------------------------|--------|
| POST | `/weather/<id>/comments` | `WeatherService.addComment(id, payload)` | ✅ |
| GET | `/weather/<id>/comments` | `WeatherService.getComments(id)` | ✅ |
| PUT | `/weather/<id>/comments/<comment_id>` | `WeatherService.updateComment(stationId, commentId, payload)` | ✅ |
| DELETE | `/weather/<id>/comments/<comment_id>` | `WeatherService.deleteComment(stationId, commentId)` | ✅ |

## Readings Endpoints (readings.py)

| Method | Backend Endpoint | Frontend Service Method | Status |
|--------|-----------------|------------------------|--------|
| POST | `/weather/<id>/readings` | `WeatherService.addReading(stationId, payload)` | ✅ |
| GET | `/weather/<id>/readings` | `WeatherService.getStationReadings(stationId, params)` | ✅ |
| PUT | `/weather/<id>/readings/<reading_id>` | `WeatherService.updateReading(stationId, readingId, payload)` | ✅ |
| DELETE | `/weather/<id>/readings/<reading_id>` | `WeatherService.deleteReading(stationId, readingId)` | ✅ |

## Summary

**Total Backend Endpoints:** 21
**Total Frontend Methods:** 21
**Coverage:** 100% ✅

All backend API endpoints are now mapped to frontend service methods!

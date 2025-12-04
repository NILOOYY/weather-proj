import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class WeatherService {

  private baseURL = 'http://127.0.0.1:5000';

  constructor(private http: HttpClient) {}

  // GET ALL WEATHER
  getWeatherList(): Observable<any> {
    return this.http.get(`${this.baseURL}/weather`);
  }

  // GET ONE WEATHER DETAIL
  getWeatherDetail(id: string): Observable<any> {
    return this.http.get(`${this.baseURL}/weather/${id}`);
  }

  // GET ALL ALERTS (with optional query string)
  getAlerts(queryString: string = ''): Observable<any> {
    return this.http.get(`${this.baseURL}/weather/alerts${queryString}`);
  }

  // GET GLOBAL TRENDS
  getTrends(): Observable<any> {
    return this.http.get(`${this.baseURL}/weather/trends/all`);
  }

  // ⭐ GET COMMENTS FOR A WEATHER RECORD
  getComments(id: string): Observable<any> {
    return this.http.get(`${this.baseURL}/weather/${id}/comments`);
  }

  // ⭐ ADD COMMENT TO WEATHER RECORD
  addComment(id: string, payload: any): Observable<any> {
    return this.http.post(`${this.baseURL}/weather/${id}/comments`, payload);
  }

  // GET READINGS FOR TREND PAGE
  getReadings(id: string): Observable<any> {
    return this.http.get(`${this.baseURL}/weather/${id}/trends`);
  }

  // ========== ADMIN WEATHER MANAGEMENT ==========

  // ADD NEW WEATHER STATION (Admin only)
  addWeatherStation(formData: FormData): Observable<any> {
    return this.http.post(`${this.baseURL}/weather`, formData);
  }

  // UPDATE WEATHER STATION (Admin only)
  updateWeatherStation(id: string, formData: FormData): Observable<any> {
    return this.http.put(`${this.baseURL}/weather/${id}`, formData);
  }

  // DELETE WEATHER STATION (Admin only)
  deleteWeatherStation(id: string): Observable<any> {
    return this.http.delete(`${this.baseURL}/weather/${id}`);
  }

  // ========== WEATHER STATS & ANALYTICS ==========

  // GET WEATHER STATS BY REGION/STATE/PLACE
  getWeatherStats(params: { region?: string; state?: string; place?: string }): Observable<any> {
    const queryParams = new URLSearchParams();
    if (params.region) queryParams.append('region', params.region);
    if (params.state) queryParams.append('state', params.state);
    if (params.place) queryParams.append('place', params.place);
    
    const queryString = queryParams.toString() ? `?${queryParams.toString()}` : '';
    return this.http.get(`${this.baseURL}/weather/stats${queryString}`);
  }

  // GET SINGLE STATION TRENDS
  getStationTrends(id: string): Observable<any> {
    return this.http.get(`${this.baseURL}/weather/${id}/trends`);
  }

  // ========== COMMENTS MANAGEMENT ==========

  // UPDATE COMMENT (Auth required)
  updateComment(stationId: string, commentId: string, payload: any): Observable<any> {
    return this.http.put(`${this.baseURL}/weather/${stationId}/comments/${commentId}`, payload);
  }

  // DELETE COMMENT (Auth required)
  deleteComment(stationId: string, commentId: string): Observable<any> {
    return this.http.delete(`${this.baseURL}/weather/${stationId}/comments/${commentId}`);
  }

  // ========== READINGS MANAGEMENT ==========

  // GET ALL READINGS FOR A STATION
  getStationReadings(stationId: string, params?: { from?: string; to?: string }): Observable<any> {
    let queryString = '';
    if (params) {
      const queryParams = new URLSearchParams();
      if (params.from) queryParams.append('from', params.from);
      if (params.to) queryParams.append('to', params.to);
      queryString = queryParams.toString() ? `?${queryParams.toString()}` : '';
    }
    return this.http.get(`${this.baseURL}/weather/${stationId}/readings${queryString}`);
  }

  // ADD READING TO STATION (Auth required)
  addReading(stationId: string, payload: any): Observable<any> {
    return this.http.post(`${this.baseURL}/weather/${stationId}/readings`, payload);
  }

  // UPDATE READING (Auth required)
  updateReading(stationId: string, readingId: string, payload: any): Observable<any> {
    return this.http.put(`${this.baseURL}/weather/${stationId}/readings/${readingId}`, payload);
  }

  // DELETE READING (Auth required)
  deleteReading(stationId: string, readingId: string): Observable<any> {
    return this.http.delete(`${this.baseURL}/weather/${stationId}/readings/${readingId}`);
  }
}


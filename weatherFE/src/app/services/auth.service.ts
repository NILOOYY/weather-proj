import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private baseURL = 'http://127.0.0.1:5000';
  private tokenKey = 'token';

  constructor(private http: HttpClient) {}

  // ------------------------------------------------
  // LOGIN USING BASIC AUTH (Flask expects BasicAuth)
  // ------------------------------------------------
  login(username: string, password: string): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: 'Basic ' + btoa(`${username}:${password}`)
    });

    return this.http.post(`${this.baseURL}/login`, {}, { headers });
  }

  // ------------------------------------------------
  // REGISTER USING FORM-DATA (Flask expects request.form)
  // ------------------------------------------------
  register(data: any): Observable<any> {
    const formData = new FormData();
    formData.append("username", data.username);
    formData.append("password", data.password);
    formData.append("admin", data.admin ? "true" : "false");

    return this.http.post(`${this.baseURL}/register`, formData);
  }

  // ------------------------------------------------
  // TOKEN HELPERS
  // ------------------------------------------------
  saveToken(token: string): void {
    localStorage.setItem(this.tokenKey, token);
  }

  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  logout(): void {
    localStorage.removeItem(this.tokenKey);
  }

  isLoggedIn(): boolean {
    return !!localStorage.getItem(this.tokenKey);
  }

  // ------------------------------------------------
  // DECODE TOKEN → CHECK ADMIN STATUS
  // ------------------------------------------------
  isAdmin(): boolean {
    const token = this.getToken();
    if (!token) return false;

    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.admin === true; // backend sets admin true/false
    } catch {
      return false;
    }
  }

  // ------------------------------------------------
  // GET USERNAME FROM TOKEN
  // ------------------------------------------------
  getUsername(): string | null {
    const token = this.getToken();
    if (!token) return null;

    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.user || null;
    } catch {
      return null;
    }
  }

  // ------------------------------------------------
  // LOGOUT WITH BACKEND (Blacklist token)
  // ------------------------------------------------
  logoutWithBackend(): Observable<any> {
    return this.http.post(`${this.baseURL}/logout`, {});
  }

  // ------------------------------------------------
  // REFRESH TOKEN
  // ------------------------------------------------
  refreshToken(): Observable<any> {
    return this.http.post(`${this.baseURL}/token/refresh`, {});
  }
}

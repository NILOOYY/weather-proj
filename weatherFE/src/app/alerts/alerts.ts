import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { WeatherService } from '../services/weather.service';

@Component({
  selector: 'app-alerts',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './alerts.html',
  styleUrl: './alerts.css',
})
export class AlertsComponent implements OnInit {

  alerts: any[] = [];
  loading: boolean = true;
  summary: any = {};
  filterRegion: string = "";
  filterState: string = "";
  filterCity: string = "";

  Object = Object; // Make Object available in template

  constructor(private weatherAPI: WeatherService) {}

  ngOnInit() {
    this.loadAlerts();
  }

  loadAlerts() {
    this.loading = true;
    let url = '';
    
    const params: string[] = [];
    if (this.filterRegion) params.push(`region=${this.filterRegion}`);
    if (this.filterState) params.push(`state=${this.filterState}`);
    if (this.filterCity) params.push(`city=${this.filterCity}`);
    
    const queryString = params.length > 0 ? `?${params.join('&')}` : '';

    this.weatherAPI.getAlerts(queryString).subscribe({
      next: (data) => {
        this.alerts = data.alerts || [];
        this.summary = data.summary_by_alert_type || {};
        this.loading = false;
      },
      error: (err) => {
        console.error("Error loading alerts:", err);
        this.loading = false;
      }
    });
  }

  applyFilters() {
    this.loadAlerts();
  }

  clearFilters() {
    this.filterRegion = "";
    this.filterState = "";
    this.filterCity = "";
    this.loadAlerts();
  }
}

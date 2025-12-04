import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { WeatherService } from '../services/weather.service';

@Component({
  selector: 'app-trends',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './trends.html',
  styleUrl: './trends.css',
})
export class TrendsComponent implements OnInit {

  trends: any = null;
  loading: boolean = true;

  constructor(private weatherAPI: WeatherService) {}

  ngOnInit() {
    this.weatherAPI.getTrends().subscribe({
      next: (data) => {
        this.trends = data;
        this.loading = false;
      },
      error: (err) => {
        console.error("Error loading trends:", err);
        this.loading = false;
      }
    });
  }
}

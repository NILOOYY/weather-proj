import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { WeatherService } from '../services/weather.service';

@Component({
  selector: 'app-weather-list',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './weather-list.html',
  styleUrl: './weather-list.css',
})
export class WeatherListComponent implements OnInit {

  weatherList: any[] = [];
  loading: boolean = true;

  constructor(private weatherAPI: WeatherService) {}

  ngOnInit() {
    this.weatherAPI.getWeatherList().subscribe({
      next: (data) => {
        this.weatherList = data.data;   // array of weather docs
        this.loading = false;

        console.log("Weather list:", this.weatherList);
      },
      error: (err) => {
        console.error("Error loading weather list", err);
        this.loading = false;
      }
    });
  }

}

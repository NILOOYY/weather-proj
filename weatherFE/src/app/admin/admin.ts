import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { WeatherService } from '../services/weather.service';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-admin',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './admin.html',
  styleUrl: './admin.css'
})
export class AdminComponent implements OnInit {

  weatherList: any[] = [];
  loading: boolean = true;
  showAddForm: boolean = false;
  editingStation: any = null;

  // Add/Edit form data
  stationForm = {
    station_name: '',
    city: '',
    state: '',
    region: '',
    place: '',
    country: '',
    latitude: '',
    longitude: '',
    avg_temp_c: '',
    max_wind_kmh: '',
    overall_condition: '',
    air_quality_index: ''
  };

  constructor(
    private weatherService: WeatherService,
    private authService: AuthService
  ) {}

  ngOnInit() {
    this.loadWeatherStations();
  }

  loadWeatherStations() {
    this.loading = true;
    this.weatherService.getWeatherList().subscribe({
      next: (data) => {
        this.weatherList = data.data || [];
        this.loading = false;
      },
      error: (err) => {
        console.error('Error loading stations:', err);
        this.loading = false;
      }
    });
  }

  // ADD NEW STATION
  showAddStationForm() {
    this.showAddForm = true;
    this.editingStation = null;
    this.resetForm();
  }

  addStation() {
    const formData = new FormData();
    Object.keys(this.stationForm).forEach(key => {
      if (this.stationForm[key as keyof typeof this.stationForm]) {
        formData.append(key, this.stationForm[key as keyof typeof this.stationForm]);
      }
    });

    this.weatherService.addWeatherStation(formData).subscribe({
      next: (response) => {
        console.log('Station added successfully:', response);
        this.showAddForm = false;
        this.loadWeatherStations();
        this.resetForm();
      },
      error: (err) => {
        console.error('Error adding station:', err);
        alert('Error adding station: ' + (err.error?.Error || 'Unknown error'));
      }
    });
  }

  // EDIT STATION
  editStation(station: any) {
    this.editingStation = station;
    this.showAddForm = true;
    
    // Populate form with existing data
    this.stationForm = {
      station_name: station.station_name || '',
      city: station.city || '',
      state: station.state || '',
      region: station.region || '',
      place: station.place || '',
      country: station.country || '',
      latitude: station.latitude || '',
      longitude: station.longitude || '',
      avg_temp_c: station.avg_temp_c || '',
      max_wind_kmh: station.max_wind_kmh || '',
      overall_condition: station.overall_condition || '',
      air_quality_index: station.air_quality_index || ''
    };
  }

  updateStation() {
    if (!this.editingStation) return;

    const formData = new FormData();
    Object.keys(this.stationForm).forEach(key => {
      if (this.stationForm[key as keyof typeof this.stationForm]) {
        formData.append(key, this.stationForm[key as keyof typeof this.stationForm]);
      }
    });

    this.weatherService.updateWeatherStation(this.editingStation._id, formData).subscribe({
      next: (response) => {
        console.log('Station updated successfully:', response);
        this.showAddForm = false;
        this.editingStation = null;
        this.loadWeatherStations();
        this.resetForm();
      },
      error: (err) => {
        console.error('Error updating station:', err);
        alert('Error updating station: ' + (err.error?.Error || 'Unknown error'));
      }
    });
  }

  // DELETE STATION
  deleteStation(station: any) {
    if (confirm(`Are you sure you want to delete "${station.station_name}" in ${station.city}?`)) {
      this.weatherService.deleteWeatherStation(station._id).subscribe({
        next: (response) => {
          console.log('Station deleted successfully:', response);
          this.loadWeatherStations();
        },
        error: (err) => {
          console.error('Error deleting station:', err);
          alert('Error deleting station: ' + (err.error?.Error || 'Unknown error'));
        }
      });
    }
  }

  // FORM HELPERS
  resetForm() {
    this.stationForm = {
      station_name: '',
      city: '',
      state: '',
      region: '',
      place: '',
      country: '',
      latitude: '',
      longitude: '',
      avg_temp_c: '',
      max_wind_kmh: '',
      overall_condition: '',
      air_quality_index: ''
    };
  }

  cancelForm() {
    this.showAddForm = false;
    this.editingStation = null;
    this.resetForm();
  }

  submitForm() {
    if (this.editingStation) {
      this.updateStation();
    } else {
      this.addStation();
    }
  }
}
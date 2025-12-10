import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, ActivatedRoute } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { WeatherService } from '../services/weather.service';
import { AuthService } from '../services/auth.service';
import { GoogleMapsModule } from '@angular/google-maps';

@Component({
  selector: 'app-weather-detail',
  standalone: true,
  imports: [CommonModule, RouterLink, FormsModule, GoogleMapsModule],
  templateUrl: './weather-detail.html',
  styleUrl: './weather-detail.css',
})
export class WeatherDetailComponent implements OnInit {

  // WEATHER DATA
  weather: any = null;

  // COMMENTS
  comments: any[] = [];
  newComment: string = "";
  newUsername: string = "";  // REQUIRED for ngModel
  newRating: number = 0;     // Optional but included

  // ID
  id: string | null = null;

  // MAP PROPERTIES
  mapCenter: google.maps.LatLngLiteral | null = null;
  mapZoom: number = 8;
  markerPosition: google.maps.LatLngLiteral | null = null;

  constructor(
    private route: ActivatedRoute,
    private weatherAPI: WeatherService,
    public authService: AuthService
  ) {}

  ngOnInit() {
    this.id = this.route.snapshot.paramMap.get('id');
    if (!this.id) return;

    this.loadWeather();
    this.loadComments();
  }

  // ⭐ LOAD WEATHER DETAILS
  loadWeather() {
    this.weatherAPI.getWeatherDetail(this.id!).subscribe({
      next: (data) => {
        this.weather = data;

        // ⭐ Map using REAL LAT + LNG fields
        if (data.latitude && data.longitude) {
          this.mapCenter = {
            lat: Number(data.latitude),
            lng: Number(data.longitude),
          };

          this.markerPosition = { ...this.mapCenter };
        }
      },
      error: (err) => console.error("Error loading weather detail:", err)
    });
  }

  // ⭐ LOAD COMMENTS FROM BACKEND
  loadComments() {
    this.weatherAPI.getComments(this.id!).subscribe({
      next: (res) => {
        this.comments = res.comments || [];
      },
      error: (err) => console.error("Error loading comments:", err)
    });
  }

  // ⭐ SUBMIT COMMENT
  submitComment() {
    if (!this.newUsername.trim() || !this.newComment.trim()) return;

    const payload = {
      username: this.newUsername,
      comment: this.newComment,
      rating: this.newRating
    };

    this.weatherAPI.addComment(this.id!, payload).subscribe({
      next: () => {
        // Clear input boxes
        this.newComment = "";
        this.newUsername = "";
        this.newRating = 0;

        // Reload comments
        this.loadComments();
      },
      error: (err) => console.error("Error posting comment:", err)
    });
  }

  // ⭐ DELETE COMMENT
  deleteComment(commentId: string) {
    if (confirm('Are you sure you want to delete this comment?')) {
      this.weatherAPI.deleteComment(this.id!, commentId).subscribe({
        next: () => {
          console.log('Comment deleted successfully');
          this.loadComments();
        },
        error: (err) => console.error("Error deleting comment:", err)
      });
    }
  }

  // ⭐ EDIT COMMENT (Simple implementation)
  editComment(comment: any) {
    const newCommentText = prompt('Edit your comment:', comment.comment);
    if (newCommentText && newCommentText.trim() !== comment.comment) {
      const payload = {
        comment: newCommentText.trim(),
        rating: comment.rating
      };

      this.weatherAPI.updateComment(this.id!, comment._id, payload).subscribe({
        next: () => {
          console.log('Comment updated successfully');
          this.loadComments();
        },
        error: (err) => console.error("Error updating comment:", err)
      });
    }
  }
}




import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './register.html',
  styleUrls: ['./register.css']
})
export class RegisterComponent {

  username: string = "";
  password: string = "";
  admin: boolean = false;

  errorMessage: string = "";
  successMessage: string = "";

  constructor(private auth: AuthService, private router: Router) {}

  register() {

    const payload = {
      username: this.username,
      password: this.password,
      admin: this.admin
    };

    this.auth.register(payload).subscribe({
      next: () => {
        this.successMessage = "Registration successful!";
        this.errorMessage = "";
        this.router.navigate(['/login']);
      },
      error: (err) => {
        this.successMessage = "";
        this.errorMessage = err.error?.Error || "Registration failed. Try again.";
      }
    });
  }
}


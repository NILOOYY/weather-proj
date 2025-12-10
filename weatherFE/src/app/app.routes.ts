import { Routes } from '@angular/router';

import { HomeComponent } from './home/home';
import { WeatherListComponent } from './weather-list/weather-list';
import { WeatherDetailComponent } from './weather-detail/weather-detail';
import { AlertsComponent } from './alerts/alerts';
import { TrendsComponent } from './trends/trends';
import { LoginComponent } from './login/login';
import { RegisterComponent } from './register/register';
import { AdminComponent } from './admin/admin';

import { UserGuard } from './guards/user.guard';
import { AdminGuard } from './guards/admin.guard';

export const routes: Routes = [
  { path: 'home', component: HomeComponent },

  // public
  { path: 'weather', component: WeatherListComponent },

  // protected: must be logged in
  { path: 'weather/:id', component: WeatherDetailComponent, canActivate: [UserGuard] },

  { path: 'alerts', component: AlertsComponent },
  { path: 'trends', component: TrendsComponent },

  // auth pages
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },

  // admin only
  { path: 'admin', component: AdminComponent, canActivate: [AdminGuard] },

  // default
  { path: '', redirectTo: 'home', pathMatch: 'full' }
];


import { Routes } from '@angular/router';

import { HomeComponent } from './home/home';
import { WeatherListComponent } from './weather-list/weather-list';
import { WeatherDetailComponent } from './weather-detail/weather-detail';
import { AlertsComponent } from './alerts/alerts';
import { TrendsComponent } from './trends/trends';
import { LoginComponent } from './login/login';
import { RegisterComponent } from './register/register';

export const routes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: 'weather', component: WeatherListComponent },
  { path: 'weather/:id', component: WeatherDetailComponent },
  { path: 'alerts', component: AlertsComponent },
  { path: 'trends', component: TrendsComponent },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: '', redirectTo: 'home', pathMatch: 'full' }
];


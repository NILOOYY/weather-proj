import { Injectable } from '@angular/core';
import {
  HttpInterceptor,
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpErrorResponse
} from '@angular/common/http';

import { Observable, catchError, switchMap, throwError } from 'rxjs';
import { AuthService } from '../services/auth.service';

@Injectable()
export class AuthRefreshInterceptor implements HttpInterceptor {

  constructor(private auth: AuthService) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {

    return next.handle(req).pipe(
      catchError((error: HttpErrorResponse) => {

        if (error.status === 401 && this.auth.isLoggedIn()) {
          return this.auth.refreshToken().pipe(
            switchMap((res: any) => {
              this.auth.saveToken(res.token);

              const cloned = req.clone({
                setHeaders: { Authorization: `Bearer ${res.token}` }
              });

              return next.handle(cloned);
            })
          );
        }

        return throwError(() => error);
      })
    );
  }
}

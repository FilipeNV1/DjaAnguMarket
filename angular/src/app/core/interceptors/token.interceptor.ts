import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { catchError, switchMap, throwError } from 'rxjs';
import { environment } from '../../../environments/environment';
import { AuthService } from '../services/auth.service';

export const tokenInterceptor: HttpInterceptorFn = (req, next) => {
  const auth = inject(AuthService);
  const router = inject(Router);
  const http = inject(HttpClient);

  const token = auth.getAccessToken();
  const authReq = token
    ? req.clone({ setHeaders: { Authorization: `Bearer ${token}` } })
    : req;

  return next(authReq).pipe(
    catchError(err => {
      if (err.status === 401 && !req.url.includes('/token/')) {
        const refresh = auth.getRefreshToken();
        if (refresh) {
          return http
            .post<{ access: string }>(`${environment.apiUrl}/token/refresh/`, { refresh })
            .pipe(
              switchMap(tokens => {
                auth.setAccessToken(tokens.access);
                const retried = req.clone({ setHeaders: { Authorization: `Bearer ${tokens.access}` } });
                return next(retried);
              }),
              catchError(() => {
                auth.logout();
                router.navigate(['/login']);
                return throwError(() => err);
              })
            );
        }
        auth.logout();
        router.navigate(['/login']);
      }
      return throwError(() => err);
    })
  );
};

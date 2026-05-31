import { environment } from '../../../environments/environment';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, of, tap, throwError } from 'rxjs';
import { Me } from '../models';

const API = environment.apiUrl;
const ACCESS_KEY = 'access_token';
const REFRESH_KEY = 'refresh_token';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private currentUser$ = new BehaviorSubject<Me | null>(null);

  constructor(private http: HttpClient) {}

  login(enumber: number, password: string): Observable<{ access: string; refresh: string }> {
    return this.http.post<{ access: string; refresh: string }>(`${API}/token/`, { enumber, password }).pipe(
      tap(tokens => {
        this.clearUser();
        localStorage.setItem(ACCESS_KEY, tokens.access);
        localStorage.setItem(REFRESH_KEY, tokens.refresh);
      })
    );
  }

  logout(): void {
    localStorage.removeItem(ACCESS_KEY);
    localStorage.removeItem(REFRESH_KEY);
    this.currentUser$.next(null);
  }

  getAccessToken(): string | null {
    return localStorage.getItem(ACCESS_KEY);
  }

  getRefreshToken(): string | null {
    return localStorage.getItem(REFRESH_KEY);
  }

  setAccessToken(token: string): void {
    localStorage.setItem(ACCESS_KEY, token);
  }

  isLoggedIn(): boolean {
    return !!this.getAccessToken();
  }

  get user$() {
    return this.currentUser$.asObservable();
  }

  getCurrentUser(forceRefresh = false): Observable<Me> {
    if (!this.isLoggedIn()) {
      return throwError(() => new Error('Not logged in'));
    }
    if (!forceRefresh && this.currentUser$.value) {
      return of(this.currentUser$.value);
    }
    return this.http.get<Me>(`${API}/me/`).pipe(
      tap(user => this.currentUser$.next(user))
    );
  }

  getUserGroup(): string | null {
    return this.currentUser$.value?.group ?? null;
  }

  clearUser(): void {
    this.currentUser$.next(null);
  }

  changePassword(old_password: string, new_password: string): Observable<{ detail: string }> {
    return this.http.post<{ detail: string }>(`${API}/me/password/`, { old_password, new_password });
  }

  updateProfile(data: Partial<Me>): Observable<Me> {
    return this.http.patch<Me>(`${API}/me/`, data).pipe(
      tap(user => this.currentUser$.next(user))
    );
  }
}

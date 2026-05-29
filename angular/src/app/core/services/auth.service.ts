import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { Me } from '../models';

const API = 'http://localhost:8000/api';
const ACCESS_KEY = 'access_token';
const REFRESH_KEY = 'refresh_token';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private currentUser$ = new BehaviorSubject<Me | null>(null);

  constructor(private http: HttpClient) {}

  login(enumber: number, password: string): Observable<{ access: string; refresh: string }> {
    return this.http.post<{ access: string; refresh: string }>(`${API}/token/`, { enumber, password }).pipe(
      tap(tokens => {
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

  getCurrentUser(): Observable<Me> {
    if (this.currentUser$.value) {
      return this.currentUser$.asObservable() as Observable<Me>;
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
}

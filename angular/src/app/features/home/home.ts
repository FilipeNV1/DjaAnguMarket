import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../core/services/auth.service';
import { Me } from '../../core/models';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './home.html',
})
export class HomeComponent implements OnInit {
  user: Me | null = null;

  constructor(private auth: AuthService) {}

  ngOnInit(): void {
    this.auth.getCurrentUser().subscribe(u => (this.user = u));
  }
}

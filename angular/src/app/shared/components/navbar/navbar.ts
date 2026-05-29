import { Component, OnInit } from '@angular/core';
import { Router, RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
import { Me } from '../../../core/models';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [RouterLink, RouterLinkActive],
  templateUrl: './navbar.html',
})
export class NavbarComponent implements OnInit {
  user: Me | null = null;

  constructor(private auth: AuthService, private router: Router) {}

  ngOnInit(): void {
    if (this.auth.isLoggedIn()) {
      this.auth.getCurrentUser().subscribe(u => (this.user = u));
    }
  }

  logout(): void {
    this.auth.logout();
    this.router.navigate(['/login']);
  }

  get isEmployee(): boolean { return this.user?.group === 'Employee'; }
  get isCashier(): boolean { return this.user?.group === 'Cashier'; }
  get isManager(): boolean { return this.user?.group === 'Manager'; }
  get isCEO(): boolean { return this.user?.group === 'CEO'; }
  get canManage(): boolean { return this.isCEO || this.isManager; }
}

import { Component, OnInit } from '@angular/core';
import { Router, RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
import { Me } from '../../../core/models';
import { NAV_ITEMS, NavItem, navItemsForGroup } from '../../../core/utils/role-access';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [RouterLink, RouterLinkActive],
  templateUrl: './navbar.html',
})
export class NavbarComponent implements OnInit {

  user: Me | null = null;
  menuItems: NavItem[] = [];

  constructor(private auth: AuthService, private router: Router) {}

  ngOnInit(): void {
    this.auth.user$.subscribe(u => {
      this.user = u;
      this.menuItems = u ? navItemsForGroup(u.group) : NAV_ITEMS;
    });
    if (this.auth.isLoggedIn()) {
      this.auth.getCurrentUser(true).subscribe();
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


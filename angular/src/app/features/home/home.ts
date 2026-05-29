import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../core/services/auth.service';
import { Me } from '../../core/models';
import { RouterLink } from '@angular/router';
import { userSubtitle } from '../../core/utils/user-display';
import { NavItem, navItemsForGroup } from '../../core/utils/role-access';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './home.html',
})
export class HomeComponent implements OnInit {
  user: Me | null = null;
  menuItems: NavItem[] = [];
  userSubtitle = userSubtitle;

  constructor(private auth: AuthService) {}

  ngOnInit(): void {
    this.auth.getCurrentUser(true).subscribe(u => {
      this.user = u;
      this.menuItems = navItemsForGroup(u.group);
    });
  }
}

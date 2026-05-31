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

  cardBorderColors = ['#0c3324', '#60a249', '#8bda4b'];
  cardBgColors     = ['rgba(12,51,36,0.08)', 'rgba(96,162,73,0.10)', 'rgba(139,218,75,0.15)'];
  cardIconColors   = ['#0c3324', '#60a249', '#60a249'];

  constructor(private auth: AuthService) {}

  ngOnInit(): void {
    this.auth.getCurrentUser(true).subscribe(u => {
      this.user = u;
      this.menuItems = navItemsForGroup(u.group);
    });
  }
}

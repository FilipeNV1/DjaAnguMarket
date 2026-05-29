import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { Distributor, Me } from '../../../core/models';

@Component({
  selector: 'app-distributor-list',
  standalone: true,
  imports: [RouterLink, FormsModule],
  templateUrl: './distributor-list.html',
})
export class DistributorListComponent implements OnInit {
  items: Distributor[] = [];
  filtered: Distributor[] = [];
  user: Me | null = null;
  search = '';

  constructor(private api: ApiService, private auth: AuthService) {}

  ngOnInit(): void {
    this.api.getDistributors().subscribe(data => { this.items = data; this.applyFilter(); });
    this.auth.getCurrentUser().subscribe(u => (this.user = u));
  }

  applyFilter(): void {
    const q = this.search.toLowerCase();
    this.filtered = q
      ? this.items.filter(i => i.name.toLowerCase().includes(q) || i.email.toLowerCase().includes(q))
      : [...this.items];
  }

  get canWrite(): boolean { return this.user?.group === 'CEO'; }

  delete(email: string): void {
    if (!confirm(`Delete distributor "${email}"?`)) return;
    this.api.deleteDistributor(email).subscribe(() => {
      this.items = this.items.filter(i => i.email !== email);
      this.applyFilter();
    });
  }
}

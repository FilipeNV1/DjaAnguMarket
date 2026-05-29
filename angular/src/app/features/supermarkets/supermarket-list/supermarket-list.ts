import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { Supermarket, Me } from '../../../core/models';

@Component({
  selector: 'app-supermarket-list',
  standalone: true,
  imports: [RouterLink, FormsModule],
  templateUrl: './supermarket-list.html',
})
export class SupermarketListComponent implements OnInit {
  items: Supermarket[] = [];
  filtered: Supermarket[] = [];
  user: Me | null = null;
  search = '';

  constructor(private api: ApiService, private auth: AuthService) {}

  ngOnInit(): void {
    this.api.getSupermarkets().subscribe(data => { this.items = data; this.applyFilter(); });
    this.auth.getCurrentUser().subscribe(u => (this.user = u));
  }

  applyFilter(): void {
    const q = this.search.toLowerCase();
    this.filtered = q ? this.items.filter(i => i.location.toLowerCase().includes(q)) : [...this.items];
  }

  get canWrite(): boolean { return this.user?.group === 'CEO' || this.user?.group === 'Manager'; }

  delete(id: number): void {
    if (!confirm('Delete this supermarket?')) return;
    this.api.deleteSupermarket(id).subscribe(() => {
      this.items = this.items.filter(i => i.id !== id);
      this.applyFilter();
    });
  }
}

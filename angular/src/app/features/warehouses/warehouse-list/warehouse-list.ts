import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { Warehouse, Me } from '../../../core/models';

@Component({
  selector: 'app-warehouse-list',
  standalone: true,
  imports: [RouterLink, FormsModule],
  templateUrl: './warehouse-list.html',
})
export class WarehouseListComponent implements OnInit {
  items: Warehouse[] = [];
  filtered: Warehouse[] = [];
  user: Me | null = null;
  search = '';

  constructor(private api: ApiService, private auth: AuthService) {}

  ngOnInit(): void {
    this.api.getWarehouses().subscribe(data => { this.items = data; this.applyFilter(); });
    this.auth.getCurrentUser().subscribe(u => (this.user = u));
  }

  applyFilter(): void {
    const q = this.search.toLowerCase();
    this.filtered = q
      ? this.items.filter(i => i.supermarket_location?.toLowerCase().includes(q) || String(i.wnumber).includes(q))
      : [...this.items];
  }

  get canWrite(): boolean { return this.user?.group === 'CEO' || this.user?.group === 'Manager'; }

  delete(id: number): void {
    if (!confirm('Delete this warehouse?')) return;
    this.api.deleteWarehouse(id).subscribe(() => {
      this.items = this.items.filter(i => i.wnumber !== id);
      this.applyFilter();
    });
  }
}

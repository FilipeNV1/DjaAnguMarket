import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { Warehouse, Me } from '../../../core/models';
import { loadList } from '../../../core/utils/list-load';

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
  loading = true;
  error = '';

  constructor(private api: ApiService, private auth: AuthService) {}

  ngOnInit(): void {
    this.load();
    this.auth.getCurrentUser().subscribe(u => (this.user = u));
  }

  load(): void {
    loadList(() => this.api.getWarehouses(), {
      onData: data => { this.items = data; this.applyFilter(); },
      onLoading: v => (this.loading = v),
      onError: msg => (this.error = msg),
    });
  }

  applyFilter(): void {
    const q = this.search.trim().toLowerCase();
    this.filtered = q
      ? this.items.filter(i => i.supermarket_location?.toLowerCase().includes(q) || String(i.wnumber).includes(q))
      : this.items;
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

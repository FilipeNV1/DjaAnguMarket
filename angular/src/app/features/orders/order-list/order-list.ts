import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { DecimalPipe } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { Order, Me } from '../../../core/models';
import { loadList } from '../../../core/utils/list-load';

@Component({
  selector: 'app-order-list',
  standalone: true,
  imports: [RouterLink, FormsModule, DecimalPipe],
  templateUrl: './order-list.html',
})
export class OrderListComponent implements OnInit {

  items: Order[] = [];
  filtered: Order[] = [];
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
    loadList(() => this.api.getOrders(), {
      onData: data => { this.items = data; this.applyFilter(); },
      onLoading: v => (this.loading = v),
      onError: msg => (this.error = msg),
    });
  }

  applyFilter(): void {
    const q = this.search.trim().toLowerCase();
    this.filtered = q
      ? this.items.filter(i => i.ord_date.includes(q) || (i.distributor_name ?? '').toLowerCase().includes(q))
      : this.items;
  }

  get canWrite(): boolean { return this.user?.group === 'CEO' || this.user?.group === 'Manager'; }

  delete(id: number): void {
    if (!confirm('Delete this order?')) return;
    this.api.deleteOrder(id).subscribe(() => {
      this.items = this.items.filter(i => i.orderid !== id);
      this.applyFilter();
    });
  }
}
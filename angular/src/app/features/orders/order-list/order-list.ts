import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { DecimalPipe } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { ToastService } from '../../../core/services/toast.service';
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
  pendingDelete: number | null = null;

  constructor(private api: ApiService, private auth: AuthService, private toast: ToastService) {}

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

  requestDelete(id: number): void { this.pendingDelete = id; }
  cancelDelete(): void { this.pendingDelete = null; }

  confirmDelete(id: number): void {
    this.api.deleteOrder(id).subscribe({
      next: () => {
        this.items = this.items.filter(i => i.orderid !== id);
        this.applyFilter();
        this.pendingDelete = null;
        this.toast.show('Order deleted.');
      },
      error: () => { this.toast.show('Failed to delete order.', 'error'); this.pendingDelete = null; },
    });
  }
}

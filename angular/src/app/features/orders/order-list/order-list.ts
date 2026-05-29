import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { Order, Me } from '../../../core/models';

@Component({
  selector: 'app-order-list',
  standalone: true,
  imports: [RouterLink, FormsModule],
  templateUrl: './order-list.html',
})
export class OrderListComponent implements OnInit {
  items: Order[] = [];
  filtered: Order[] = [];
  user: Me | null = null;
  search = '';

  constructor(private api: ApiService, private auth: AuthService) {}

  ngOnInit(): void {
    this.api.getOrders().subscribe(data => { this.items = data; this.applyFilter(); });
    this.auth.getCurrentUser().subscribe(u => (this.user = u));
  }

  applyFilter(): void {
    const q = this.search.toLowerCase();
    this.filtered = q
      ? this.items.filter(i => i.ord_date.includes(q) || (i.distributor_name ?? '').toLowerCase().includes(q))
      : [...this.items];
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

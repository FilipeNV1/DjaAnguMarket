import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { DecimalPipe } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { Purchase, Me } from '../../../core/models';
import { loadList } from '../../../core/utils/list-load';

@Component({
  selector: 'app-purchase-list',
  standalone: true,
  imports: [RouterLink, FormsModule, DecimalPipe],
  templateUrl: './purchase-list.html',
})
export class PurchaseListComponent implements OnInit {

  items: Purchase[] = [];
  filtered: Purchase[] = [];
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
    loadList(() => this.api.getPurchases(), {
      onData: data => { this.items = data; this.applyFilter(); },
      onLoading: v => (this.loading = v),
      onError: msg => (this.error = msg),
    });
  }

  applyFilter(): void {
    const q = this.search.trim().toLowerCase();
    this.filtered = q
      ? this.items.filter(i => i.date.includes(q) || (i.client_name ?? '').toLowerCase().includes(q))
      : this.items;
  }

  get canCreate(): boolean { return (this.user?.group ?? '') !== 'Employee'; }

  get canManage(): boolean {
    const g = this.user?.group;
    return g === 'CEO' || g === 'Manager' || g === 'Cashier';
  }

  delete(id: number): void {
    if (!confirm('Delete this purchase?')) return;
    this.api.deletePurchase(id).subscribe(() => {
      this.items = this.items.filter(i => i.purchid !== id);
      this.applyFilter();
    });
  }
}
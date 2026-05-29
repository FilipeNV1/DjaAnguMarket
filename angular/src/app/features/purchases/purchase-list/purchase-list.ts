import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { Purchase, Me } from '../../../core/models';

@Component({
  selector: 'app-purchase-list',
  standalone: true,
  imports: [RouterLink, FormsModule],
  templateUrl: './purchase-list.html',
})
export class PurchaseListComponent implements OnInit {
  items: Purchase[] = [];
  filtered: Purchase[] = [];
  user: Me | null = null;
  search = '';

  constructor(private api: ApiService, private auth: AuthService) {}

  ngOnInit(): void {
    this.api.getPurchases().subscribe(data => { this.items = data; this.applyFilter(); });
    this.auth.getCurrentUser().subscribe(u => (this.user = u));
  }

  applyFilter(): void {
    const q = this.search.toLowerCase();
    this.filtered = q
      ? this.items.filter(i => i.date.includes(q) || (i.client_name ?? '').toLowerCase().includes(q))
      : [...this.items];
  }

  get canCreate(): boolean { return (this.user?.group ?? '') !== 'Employee'; }
  get canManage(): boolean { return this.user?.group === 'CEO' || this.user?.group === 'Manager'; }

  delete(id: number): void {
    if (!confirm('Delete this purchase?')) return;
    this.api.deletePurchase(id).subscribe(() => {
      this.items = this.items.filter(i => i.purchid !== id);
      this.applyFilter();
    });
  }
}

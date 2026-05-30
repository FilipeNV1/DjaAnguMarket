import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { DecimalPipe } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { Product, Me } from '../../../core/models';
import { loadList } from '../../../core/utils/list-load';

@Component({
  selector: 'app-product-list',
  standalone: true,
  imports: [RouterLink, FormsModule, DecimalPipe],
  templateUrl: './product-list.html',
})
export class ProductListComponent implements OnInit {
  items: Product[] = [];
  filtered: Product[] = [];
  user: Me | null = null;
  search = '';
  loading = true;
  error = '';

  constructor(private api: ApiService, private auth: AuthService) {}

  ngOnInit(): void {
    this.load();
    this.auth.getCurrentUser().subscribe({ next: u => (this.user = u) });
  }

  load(): void {
    loadList(() => this.api.getProducts(), {
      onData: data => { this.items = data; this.applyFilter(); },
      onLoading: v => (this.loading = v),
      onError: msg => (this.error = msg),
    });
  }

  applyFilter(): void {
    const q = this.search.trim().toLowerCase();
    this.filtered = q
      ? this.items.filter(i => i.name.toLowerCase().includes(q) || i.brand.toLowerCase().includes(q))
      : this.items;
  }

  get canWrite(): boolean { return this.user?.group === 'CEO'; }

  delete(id: number): void {
    if (!confirm('Delete this product?')) return;
    this.api.deleteProduct(id).subscribe(() => {
      this.items = this.items.filter(i => i.prodid !== id);
      this.applyFilter();
    });
  }
}

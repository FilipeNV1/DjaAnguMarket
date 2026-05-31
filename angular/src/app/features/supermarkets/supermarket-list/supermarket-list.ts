import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { ToastService } from '../../../core/services/toast.service';
import { Supermarket, Me } from '../../../core/models';
import { loadList } from '../../../core/utils/list-load';

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
  loading = true;
  error = '';
  pendingDelete: number | null = null;

  constructor(private api: ApiService, private auth: AuthService, private toast: ToastService) {}

  ngOnInit(): void {
    this.load();
    this.auth.getCurrentUser().subscribe(u => (this.user = u));
  }

  load(): void {
    loadList(() => this.api.getSupermarkets(), {
      onData: data => { this.items = data; this.applyFilter(); },
      onLoading: v => (this.loading = v),
      onError: msg => (this.error = msg),
    });
  }

  applyFilter(): void {
    const q = this.search.trim().toLowerCase();
    this.filtered = q ? this.items.filter(i => i.location.toLowerCase().includes(q)) : this.items;
  }

  get canWrite(): boolean { return this.user?.group === 'CEO' || this.user?.group === 'Manager'; }

  requestDelete(id: number): void { this.pendingDelete = id; }
  cancelDelete(): void { this.pendingDelete = null; }

  confirmDelete(id: number): void {
    this.api.deleteSupermarket(id).subscribe({
      next: () => {
        this.items = this.items.filter(i => i.id !== id);
        this.applyFilter();
        this.pendingDelete = null;
        this.toast.show('Supermarket deleted.');
      },
      error: () => { this.toast.show('Failed to delete supermarket.', 'error'); this.pendingDelete = null; },
    });
  }
}

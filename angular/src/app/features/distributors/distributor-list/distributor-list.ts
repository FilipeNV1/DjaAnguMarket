import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { ToastService } from '../../../core/services/toast.service';
import { Distributor, Me } from '../../../core/models';
import { loadList } from '../../../core/utils/list-load';

@Component({
  selector: 'app-distributor-list',
  standalone: true,
  imports: [RouterLink, FormsModule],
  templateUrl: './distributor-list.html',
})
export class DistributorListComponent implements OnInit {

  items: Distributor[] = [];
  filtered: Distributor[] = [];
  user: Me | null = null;
  search = '';
  loading = true;
  error = '';
  pendingDelete: string | null = null;

  constructor(private api: ApiService, private auth: AuthService, private toast: ToastService) {}

  ngOnInit(): void {
    this.load();
    this.auth.getCurrentUser().subscribe(u => (this.user = u));
  }

  load(): void {
    loadList(() => this.api.getDistributors(), {
      onData: data => { this.items = data; this.applyFilter(); },
      onLoading: v => (this.loading = v),
      onError: msg => (this.error = msg),
    });
  }

  applyFilter(): void {
    const q = this.search.trim().toLowerCase();
    this.filtered = q
      ? this.items.filter(i => i.name.toLowerCase().includes(q) || i.email.toLowerCase().includes(q))
      : this.items;
  }

  get canWrite(): boolean { return this.user?.group === 'CEO'; }

  requestDelete(email: string): void { this.pendingDelete = email; }
  cancelDelete(): void { this.pendingDelete = null; }

  confirmDelete(email: string): void {
    this.api.deleteDistributor(email).subscribe({
      next: () => {
        this.items = this.items.filter(i => i.email !== email);
        this.applyFilter();
        this.pendingDelete = null;
        this.toast.show('Distributor deleted.');
      },
      error: () => { this.toast.show('Failed to delete distributor.', 'error'); this.pendingDelete = null; },
    });
  }
}

import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { ToastService } from '../../../core/services/toast.service';
import { Client, Me } from '../../../core/models';
import { loadList } from '../../../core/utils/list-load';

@Component({
  selector: 'app-client-list',
  standalone: true,
  imports: [RouterLink, FormsModule],
  templateUrl: './client-list.html',
})
export class ClientListComponent implements OnInit {

  items: Client[] = [];
  filtered: Client[] = [];
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
    loadList(() => this.api.getClients(), {
      onData: data => { this.items = data; this.applyFilter(); },
      onLoading: v => (this.loading = v),
      onError: msg => (this.error = msg),
    });
  }

  applyFilter(): void {
    const q = this.search.trim().toLowerCase();
    this.filtered = q
      ? this.items.filter(i => i.name.toLowerCase().includes(q) || String(i.nif).includes(q))
      : this.items;
  }

  get canWrite(): boolean { return this.user?.group === 'CEO' || this.user?.group === 'Manager'; }

  requestDelete(nif: number): void { this.pendingDelete = nif; }
  cancelDelete(): void { this.pendingDelete = null; }

  confirmDelete(nif: number): void {
    this.api.deleteClient(nif).subscribe({
      next: () => {
        this.items = this.items.filter(i => i.nif !== nif);
        this.applyFilter();
        this.pendingDelete = null;
        this.toast.show('Client deleted.');
      },
      error: () => { this.toast.show('Failed to delete client.', 'error'); this.pendingDelete = null; },
    });
  }
}

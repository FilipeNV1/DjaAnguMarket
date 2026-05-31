import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
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

  constructor(private api: ApiService, private auth: AuthService) {}

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

  delete(nif: number): void {
    if (!confirm('Delete this client?')) return;
    this.api.deleteClient(nif).subscribe(() => {
      this.items = this.items.filter(i => i.nif !== nif);
      this.applyFilter();
    });
  }
}
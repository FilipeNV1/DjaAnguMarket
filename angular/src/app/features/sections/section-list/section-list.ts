import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { ToastService } from '../../../core/services/toast.service';
import { Section, Me } from '../../../core/models';
import { loadList } from '../../../core/utils/list-load';

@Component({
  selector: 'app-section-list',
  standalone: true,
  imports: [RouterLink, FormsModule],
  templateUrl: './section-list.html',
})
export class SectionListComponent implements OnInit {

  items: Section[] = [];
  filtered: Section[] = [];
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
    loadList(() => this.api.getSections(), {
      onData: data => { this.items = data; this.applyFilter(); },
      onLoading: v => (this.loading = v),
      onError: msg => (this.error = msg),
    });
  }

  applyFilter(): void {
    const q = this.search.trim().toLowerCase();
    this.filtered = q
      ? this.items.filter(i => i.sname.toLowerCase().includes(q) || i.department.toLowerCase().includes(q))
      : this.items;
  }

  get canWrite(): boolean { return this.user?.group === 'CEO'; }

  requestDelete(sname: string): void { this.pendingDelete = sname; }
  cancelDelete(): void { this.pendingDelete = null; }

  confirmDelete(sname: string): void {
    this.api.deleteSection(sname).subscribe({
      next: () => {
        this.items = this.items.filter(i => i.sname !== sname);
        this.applyFilter();
        this.pendingDelete = null;
        this.toast.show('Section deleted.');
      },
      error: () => { this.toast.show('Failed to delete section.', 'error'); this.pendingDelete = null; },
    });
  }
}

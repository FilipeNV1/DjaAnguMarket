import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { Employee, Me } from '../../../core/models';
import { isRoleSameAsGroup } from '../../../core/utils/user-display';
import { loadList } from '../../../core/utils/list-load';

@Component({
  selector: 'app-employee-list',
  standalone: true,
  imports: [RouterLink, FormsModule],
  templateUrl: './employee-list.html',
})
export class EmployeeListComponent implements OnInit {
  items: Employee[] = [];
  filtered: Employee[] = [];
  user: Me | null = null;
  search = '';
  loading = true;
  error = '';
  isRoleSameAsGroup = isRoleSameAsGroup;

  constructor(private api: ApiService, private auth: AuthService) {}

  ngOnInit(): void {
    this.load();
    this.auth.getCurrentUser().subscribe(u => (this.user = u));
  }

  load(): void {
    loadList(() => this.api.getEmployees(), {
      onData: data => { this.items = data; this.applyFilter(); },
      onLoading: v => (this.loading = v),
      onError: msg => (this.error = msg),
    });
  }

  applyFilter(): void {
    const q = this.search.trim().toLowerCase();
    this.filtered = q
      ? this.items.filter(i => i.name.toLowerCase().includes(q) || i.role.toLowerCase().includes(q))
      : this.items;
  }

  get canWrite(): boolean { return this.user?.group === 'CEO' || this.user?.group === 'Manager'; }

  delete(enumber: number): void {
    if (!confirm('Delete this employee?')) return;
    this.api.deleteEmployee(enumber).subscribe(() => {
      this.items = this.items.filter(i => i.enumber !== enumber);
      this.applyFilter();
    });
  }
}

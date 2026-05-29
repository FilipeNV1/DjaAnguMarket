import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { Employee, Me } from '../../../core/models';

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

  constructor(private api: ApiService, private auth: AuthService) {}

  ngOnInit(): void {
    this.api.getEmployees().subscribe(data => { this.items = data; this.applyFilter(); });
    this.auth.getCurrentUser().subscribe(u => (this.user = u));
  }

  applyFilter(): void {
    const q = this.search.toLowerCase();
    this.filtered = q
      ? this.items.filter(i => i.name.toLowerCase().includes(q) || i.role.toLowerCase().includes(q))
      : [...this.items];
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

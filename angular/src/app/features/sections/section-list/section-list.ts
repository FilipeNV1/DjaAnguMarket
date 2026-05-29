import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { Section, Me } from '../../../core/models';

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

  constructor(private api: ApiService, private auth: AuthService) {}

  ngOnInit(): void {
    this.api.getSections().subscribe(data => { this.items = data; this.applyFilter(); });
    this.auth.getCurrentUser().subscribe(u => (this.user = u));
  }

  applyFilter(): void {
    const q = this.search.toLowerCase();
    this.filtered = q
      ? this.items.filter(i => i.sname.toLowerCase().includes(q) || i.department.toLowerCase().includes(q))
      : [...this.items];
  }

  get canWrite(): boolean { return this.user?.group === 'CEO'; }

  delete(sname: string): void {
    if (!confirm(`Delete section "${sname}"?`)) return;
    this.api.deleteSection(sname).subscribe(() => {
      this.items = this.items.filter(i => i.sname !== sname);
      this.applyFilter();
    });
  }
}

import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { ToastService } from '../../../core/services/toast.service';
import { Section } from '../../../core/models';

@Component({
  selector: 'app-supermarket-form',
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './supermarket-form.html',
})
export class SupermarketFormComponent implements OnInit {
  form: FormGroup;
  sections: Section[] = [];
  isEditing = false;
  id: number | null = null;
  error = '';

  constructor(
    private fb: FormBuilder,
    private api: ApiService,
    private route: ActivatedRoute,
    private router: Router,
    private toast: ToastService,
  ) {
    this.form = this.fb.group({
      location: ['', Validators.required],
      opening_time: ['', Validators.required],
      close_time: ['', Validators.required],
      section_ids: [[]],
    });
  }

  ngOnInit(): void {
    this.api.getSections().subscribe(s => (this.sections = s));
    this.id = this.route.snapshot.params['id'] ? +this.route.snapshot.params['id'] : null;
    if (this.id) {
      this.isEditing = true;
      this.api.getSupermarket(this.id).subscribe(s => {
        this.form.patchValue({
          location: s.location,
          opening_time: s.opening_time,
          close_time: s.close_time,
          section_ids: s.sections.map(sec => sec.sname),
        });
      });
    }
  }

  toggleSection(sname: string): void {
    const current: string[] = this.form.value.section_ids;
    const updated = current.includes(sname)
      ? current.filter(s => s !== sname)
      : [...current, sname];
    this.form.patchValue({ section_ids: updated });
  }

  isSelected(sname: string): boolean {
    return (this.form.value.section_ids as string[]).includes(sname);
  }

  submit(): void {
    if (this.form.invalid) return;
    const data = this.form.value;
    if (data.close_time <= data.opening_time) {
      this.error = 'Close time must be after opening time.';
      return;
    }
    this.error = '';
    const req = this.isEditing
      ? this.api.updateSupermarket(this.id!, data)
      : this.api.createSupermarket(data);
    req.subscribe({
      next: () => { this.toast.show(this.isEditing ? 'Supermarket updated.' : 'Supermarket created.'); this.router.navigate(['/supermarkets']); },
      error: err => (this.error = JSON.stringify(err.error)),
    });
  }
}

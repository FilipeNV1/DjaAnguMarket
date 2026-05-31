import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { ToastService } from '../../../core/services/toast.service';

@Component({
  selector: 'app-section-form',
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './section-form.html',
})
export class SectionFormComponent implements OnInit {
  form: FormGroup;
  isEditing = false;
  sname: string | null = null;
  error = '';

  constructor(
    private fb: FormBuilder,
    private api: ApiService,
    private route: ActivatedRoute,
    private router: Router,
    private toast: ToastService,
  ) {
    this.form = this.fb.group({
      sname: ['', Validators.required],
      department: ['', Validators.required],
    });
  }

  ngOnInit(): void {
    this.sname = this.route.snapshot.params['id'] ?? null;
    if (this.sname) {
      this.isEditing = true;
      this.form.get('sname')!.disable();
      this.api.getSection(this.sname).subscribe(s => this.form.patchValue(s));
    }
  }

  submit(): void {
    if (this.form.invalid) return;
    this.error = '';
    const data = this.form.getRawValue();
    const req = this.isEditing
      ? this.api.updateSection(this.sname!, data)
      : this.api.createSection(data);
    req.subscribe({
      next: () => { this.toast.show(this.isEditing ? 'Section updated.' : 'Section created.'); this.router.navigate(['/sections']); },
      error: err => (this.error = JSON.stringify(err.error)),
    });
  }
}

import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { ToastService } from '../../../core/services/toast.service';

@Component({
  selector: 'app-distributor-form',
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './distributor-form.html',
})
export class DistributorFormComponent implements OnInit {
  form: FormGroup;
  isEditing = false;
  email: string | null = null;
  error = '';

  constructor(
    private fb: FormBuilder,
    private api: ApiService,
    private route: ActivatedRoute,
    private router: Router,
    private toast: ToastService,
  ) {
    this.form = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      name: ['', Validators.required],
      contact: ['', Validators.required],
    });
  }

  ngOnInit(): void {
    this.email = this.route.snapshot.params['id'] ?? null;
    if (this.email) {
      this.isEditing = true;
      this.form.get('email')!.disable();
      this.api.getDistributor(this.email).subscribe(d => this.form.patchValue(d));
    }
  }

  submit(): void {
    if (this.form.invalid) return;
    this.error = '';
    const data = this.form.getRawValue();
    const req = this.isEditing
      ? this.api.updateDistributor(this.email!, data)
      : this.api.createDistributor(data);
    req.subscribe({
      next: () => { this.toast.show(this.isEditing ? 'Distributor updated.' : 'Distributor created.'); this.router.navigate(['/distributors']); },
      error: err => (this.error = JSON.stringify(err.error)),
    });
  }
}

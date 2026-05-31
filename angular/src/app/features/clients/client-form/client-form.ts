import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { ToastService } from '../../../core/services/toast.service';

@Component({
  selector: 'app-client-form',
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './client-form.html',
})
export class ClientFormComponent implements OnInit {
  form: FormGroup;
  isEditing = false;
  nif: number | null = null;
  error = '';

  constructor(
    private fb: FormBuilder,
    private api: ApiService,
    private route: ActivatedRoute,
    private router: Router,
    private toast: ToastService,
  ) {
    this.form = this.fb.group({
      nif: [null, Validators.required],
      name: ['', Validators.required],
      fidelity: [0, [Validators.required, Validators.min(0)]],
      address: ['', Validators.required],
      contact: ['', Validators.required],
    });
  }

  ngOnInit(): void {
    this.nif = this.route.snapshot.params['id'] ? +this.route.snapshot.params['id'] : null;
    if (this.nif) {
      this.isEditing = true;
      this.form.get('nif')!.disable();
      this.api.getClient(this.nif).subscribe(c => this.form.patchValue(c));
    }
  }

  submit(): void {
    if (this.form.invalid) return;
    this.error = '';
    const data = this.form.getRawValue();
    const req = this.isEditing
      ? this.api.updateClient(this.nif!, data)
      : this.api.createClient(data);
    req.subscribe({
      next: () => { this.toast.show(this.isEditing ? 'Client updated.' : 'Client created.'); this.router.navigate(['/clients']); },
      error: err => (this.error = JSON.stringify(err.error)),
    });
  }
}

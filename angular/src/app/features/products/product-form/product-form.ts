import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { ToastService } from '../../../core/services/toast.service';
import { Section } from '../../../core/models';

@Component({
  selector: 'app-product-form',
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './product-form.html',
})
export class ProductFormComponent implements OnInit {
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
      name: ['', Validators.required],
      brand: ['', Validators.required],
      price: [null, [Validators.required, Validators.min(0)]],
      req_cold: [false],
      section_name: ['', Validators.required],
    });
  }

  ngOnInit(): void {
    this.api.getSections().subscribe(s => (this.sections = s));
    this.id = this.route.snapshot.params['id'] ? +this.route.snapshot.params['id'] : null;
    if (this.id) {
      this.isEditing = true;
      this.api.getProduct(this.id).subscribe(p => this.form.patchValue(p));
    }
  }

  submit(): void {
    if (this.form.invalid) return;
    this.error = '';
    const data = this.form.value;
    const req = this.isEditing
      ? this.api.updateProduct(this.id!, data)
      : this.api.createProduct(data);
    req.subscribe({
      next: () => { this.toast.show(this.isEditing ? 'Product updated.' : 'Product created.'); this.router.navigate(['/products']); },
      error: err => (this.error = JSON.stringify(err.error)),
    });
  }
}

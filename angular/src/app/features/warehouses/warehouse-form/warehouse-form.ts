import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { ToastService } from '../../../core/services/toast.service';
import { Supermarket, Product, Me } from '../../../core/models';

@Component({
  selector: 'app-warehouse-form',
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './warehouse-form.html',
})
export class WarehouseFormComponent implements OnInit {
  form: FormGroup;
  supermarkets: Supermarket[] = [];
  products: Product[] = [];
  isEditing = false;
  id: number | null = null;
  error = '';

  constructor(
    private fb: FormBuilder,
    private api: ApiService,
    private auth: AuthService,
    private route: ActivatedRoute,
    private router: Router,
    private toast: ToastService,
  ) {
    this.form = this.fb.group({
      area: [null, [Validators.required, Validators.min(1)]],
      supermarket: [null, Validators.required],
      product_ids: [[]],
    });
  }

  ngOnInit(): void {
    this.api.getSupermarkets().subscribe(s => (this.supermarkets = s));
    this.api.getProducts().subscribe(p => (this.products = p));
    this.auth.getCurrentUser().subscribe(u => {
      if (u.group !== 'CEO') {
        this.form.patchValue({ supermarket: u.supermarket_id });
        this.form.get('supermarket')!.disable();
      }
    });

    this.id = this.route.snapshot.params['id'] ? +this.route.snapshot.params['id'] : null;
    if (this.id) {
      this.isEditing = true;
      this.api.getWarehouse(this.id).subscribe(w => {
        this.form.patchValue({
          area: w.area,
          supermarket: w.supermarket,
          product_ids: w.stock?.map(s => s.product) ?? [],
        });
      });
    }
  }

  toggleProduct(id: number): void {
    const current: number[] = this.form.value.product_ids;
    this.form.patchValue({
      product_ids: current.includes(id) ? current.filter(p => p !== id) : [...current, id],
    });
  }

  isSelected(id: number): boolean {
    return (this.form.value.product_ids as number[]).includes(id);
  }

  submit(): void {
    if (this.form.invalid) return;
    this.error = '';
    const data = this.form.getRawValue();
    const req = this.isEditing
      ? this.api.updateWarehouse(this.id!, data)
      : this.api.createWarehouse(data);
    req.subscribe({
      next: () => { this.toast.show(this.isEditing ? 'Warehouse updated.' : 'Warehouse created.'); this.router.navigate(['/warehouses']); },
      error: err => (this.error = JSON.stringify(err.error)),
    });
  }
}

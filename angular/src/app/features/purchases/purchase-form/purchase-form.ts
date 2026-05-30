import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule, FormsModule } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { Supermarket, Client, Product, Me } from '../../../core/models';

interface ItemRow { product: number; quantity: number; name: string; }

@Component({
  selector: 'app-purchase-form',
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink, FormsModule],
  templateUrl: './purchase-form.html',
})
export class PurchaseFormComponent implements OnInit {
  form: FormGroup;
  supermarkets: Supermarket[] = [];
  clients: Client[] = [];
  products: Product[] = [];
  itemRows: ItemRow[] = [];
  isEditing = false;
  id: number | null = null;
  error = '';

  constructor(
    private fb: FormBuilder,
    private api: ApiService,
    private auth: AuthService,
    private route: ActivatedRoute,
    private router: Router
  ) {
    this.form = this.fb.group({
      date: [new Date().toISOString().slice(0, 10), Validators.required],
      supermarket: [null, Validators.required],
      client: [null],
    });
  }

  ngOnInit(): void {
    this.api.getSupermarkets().subscribe(s => (this.supermarkets = s));
    this.api.getClients().subscribe(c => (this.clients = c));
    this.api.getProducts().subscribe(p => (this.products = p));
    this.auth.getCurrentUser().subscribe((u: Me) => {
      if (u.group !== 'CEO') {
        this.form.patchValue({ supermarket: u.supermarket_id });
        this.form.get('supermarket')!.disable();
      }
    });

    this.id = this.route.snapshot.params['id'] ? +this.route.snapshot.params['id'] : null;
    if (this.id) {
      this.isEditing = true;
      this.api.getPurchase(this.id).subscribe(p => {
        this.form.patchValue({ date: p.date?.slice(0, 10), supermarket: p.supermarket, client: p.client });
        this.itemRows = (p.items ?? []).map(i => ({
          product: i.product,
          quantity: i.quantity,
          name: i.product_name ?? '',
        }));
      });
    }
  }

  addItem(): void {
    if (this.products.length === 0) return;
    const first = this.products[0];
    this.itemRows.push({ product: first.prodid, quantity: 1, name: first.name });
  }

  removeItem(i: number): void { this.itemRows.splice(i, 1); }

  onProductChange(index: number, prodid: number): void {
    const found = this.products.find(p => p.prodid === +prodid);
    if (found) this.itemRows[index].name = found.name;
  }

  submit(): void {
    if (this.form.invalid) return;
    if (this.itemRows.length === 0) { this.error = 'At least one product is required.'; return; }
    this.error = '';
    const data = {
      ...this.form.getRawValue(),
      item_data: this.itemRows.map(r => ({ product: r.product, quantity: r.quantity })),
    };
    const req = this.isEditing
      ? this.api.updatePurchase(this.id!, data)
      : this.api.createPurchase(data);
    req.subscribe({
      next: () => this.router.navigate(['/purchases']),
      error: err => (this.error = JSON.stringify(err.error)),
    });
  }
}

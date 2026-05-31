import { Component, OnInit, signal, computed } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule, FormsModule } from '@angular/forms';
import { DecimalPipe } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { ToastService } from '../../../core/services/toast.service';
import { Supermarket, Distributor, Product, Me } from '../../../core/models';

interface ItemRow { product: number; quantity: number; name: string; price: number; }

// Orders buy from distributors at 60% of the product price (matches the DRF
// OrderItemSerializer: discounted_price = product.price * 0.6).
const ORDER_DISCOUNT = 0.6;

@Component({
  selector: 'app-order-form',
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink, FormsModule, DecimalPipe],
  templateUrl: './order-form.html',
})
export class OrderFormComponent implements OnInit {
  form: FormGroup;
  supermarkets: Supermarket[] = [];
  distributors: Distributor[] = [];
  isEditing = false;
  id: number | null = null;
  error = '';

  // --- Reactive product-picker state, modelled with signals ---
  readonly products = signal<Product[]>([]);
  readonly itemRows = signal<ItemRow[]>([]);
  readonly showProductModal = signal(false);
  readonly modalSearch = signal('');
  readonly selectedSection = signal<string | null>(null);

  // Derived state via computed() - memoized, only recomputes when a dependency changes.
  readonly sectionNames = computed(() =>
    [...new Set(this.products().map(p => p.section ?? p.section_name).filter(Boolean))].sort((a, b) =>
      a.localeCompare(b)
    )
  );

  readonly searchResults = computed(() => {
    const q = this.modalSearch().trim().toLowerCase();
    if (!q) return [];
    return this.products().filter(
      p => p.name.toLowerCase().includes(q) || (p.brand?.toLowerCase().includes(q) ?? false)
    );
  });

  readonly sectionProducts = computed(() => {
    const section = this.selectedSection();
    if (!section) return [];
    return this.products().filter(p => (p.section ?? p.section_name) === section);
  });

  // Running total - recomputes automatically when itemRows (or any quantity) changes.
  readonly total = computed(() => this.itemRows().reduce((sum, r) => sum + r.quantity * r.price, 0));

  constructor(
    private fb: FormBuilder,
    private api: ApiService,
    private auth: AuthService,
    private route: ActivatedRoute,
    private router: Router,
    private toast: ToastService,
  ) {
    this.form = this.fb.group({
      ord_date: [new Date().toISOString().slice(0, 10), Validators.required],
      supermarket: [null, Validators.required],
      distributor: ['', Validators.required],
    });
  }

  ngOnInit(): void {
    this.api.getSupermarkets().subscribe(s => (this.supermarkets = s));
    this.api.getDistributors().subscribe(d => (this.distributors = d));
    this.api.getProducts().subscribe(p => {
      this.products.set(p);
      if (!this.selectedSection()) this.selectedSection.set(this.sectionNames()[0] ?? null);
    });
    this.auth.getCurrentUser().subscribe((u: Me) => {
      if (u.group !== 'CEO') {
        this.form.patchValue({ supermarket: u.supermarket_id });
        this.form.get('supermarket')!.disable();
      }
    });

    this.id = this.route.snapshot.params['id'] ? +this.route.snapshot.params['id'] : null;
    if (this.id) {
      this.isEditing = true;
      this.api.getOrder(this.id).subscribe(o => {
        this.form.patchValue({ ord_date: o.ord_date, supermarket: o.supermarket, distributor: o.distributor });
        this.itemRows.set(
          (o.items ?? []).map(i => ({
            product: i.product,
            quantity: i.quantity,
            name: i.product_name ?? '',
            price: i.discounted_price ?? 0,
          }))
        );
      });
    }
  }

  // --- Product picker modal ---
  openProductModal(): void {
    this.modalSearch.set('');
    if (!this.selectedSection()) this.selectedSection.set(this.sectionNames()[0] ?? null);
    this.showProductModal.set(true);
  }

  closeProductModal(): void {
    this.showProductModal.set(false);
  }

  selectSection(section: string): void {
    this.selectedSection.set(section);
  }

  isAdded(prodid: number): boolean {
    return this.itemRows().some(r => r.product === prodid);
  }

  pickProduct(p: Product): void {
    this.itemRows.update(rows => {
      if (rows.some(r => r.product === p.prodid)) {
        return rows.map(r => (r.product === p.prodid ? { ...r, quantity: r.quantity + 1 } : r));
      }
      return [...rows, { product: p.prodid, quantity: 1, name: p.name, price: p.price * ORDER_DISCOUNT }];
    });
    this.closeProductModal();
  }

  updateQuantity(prodid: number, quantity: number): void {
    this.itemRows.update(rows => rows.map(r => (r.product === prodid ? { ...r, quantity } : r)));
  }

  removeItem(prodid: number): void {
    this.itemRows.update(rows => rows.filter(r => r.product !== prodid));
  }

  submit(): void {
    if (this.form.invalid) return;
    if (this.itemRows().length === 0) { this.error = 'At least one product is required.'; return; }
    this.error = '';
    const data = {
      ...this.form.getRawValue(),
      item_data: this.itemRows().map(r => ({ product: r.product, quantity: r.quantity })),
    };
    const req = this.isEditing
      ? this.api.updateOrder(this.id!, data)
      : this.api.createOrder(data);
    req.subscribe({
      next: () => { this.toast.show(this.isEditing ? 'Order updated.' : 'Order created.'); this.router.navigate(['/orders']); },
      error: err => (this.error = JSON.stringify(err.error)),
    });
  }
}

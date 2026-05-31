import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';
import { AuthService } from '../../../core/services/auth.service';
import { ToastService } from '../../../core/services/toast.service';
import { Supermarket, Employee, Me } from '../../../core/models';

@Component({
  selector: 'app-employee-form',
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './employee-form.html',
})
export class EmployeeFormComponent implements OnInit {
  form: FormGroup;
  supermarkets: Supermarket[] = [];
  employees: Employee[] = [];
  groups = ['CEO', 'Manager', 'Cashier', 'Employee'];
  isEditing = false;
  id: number | null = null;
  error = '';
  user: Me | null = null;

  constructor(
    private fb: FormBuilder,
    private api: ApiService,
    private auth: AuthService,
    private route: ActivatedRoute,
    private router: Router,
    private toast: ToastService,
  ) {
    this.form = this.fb.group({
      name: ['', Validators.required],
      role: ['', Validators.required],
      salary: [null, [Validators.required, Validators.min(0.01)]],
      age: [null, [Validators.required, Validators.min(16)]],
      contact: ['', Validators.required],
      supermarket: [null, Validators.required],
      sex: ['M', Validators.required],
      supervisor: [null],
      is_active: [true],
      group_name: ['Employee'],
    });
  }

  ngOnInit(): void {
    this.auth.getCurrentUser().subscribe(u => {
      this.user = u;
      if (u.group !== 'CEO') {
        this.form.patchValue({ supermarket: u.supermarket_id });
        this.form.get('supermarket')!.disable();
      }
    });
    this.api.getSupermarkets().subscribe(s => (this.supermarkets = s));
    this.api.getEmployees().subscribe(e => (this.employees = e));

    this.id = this.route.snapshot.params['id'] ? +this.route.snapshot.params['id'] : null;
    if (this.id) {
      this.isEditing = true;
      this.api.getEmployee(this.id).subscribe(e => {
        this.form.patchValue({
          name: e.name,
          role: e.role,
          salary: e.salary,
          age: e.age,
          contact: e.contact,
          supermarket: e.supermarket,
          sex: e.sex,
          supervisor: e.supervisor,
          is_active: e.is_active,
          group_name: e.group ?? 'Employee',
        });
      });
    }
  }

  submit(): void {
    if (this.form.invalid) return;
    this.error = '';
    const raw = this.form.getRawValue();
    const toNullableInt = (v: unknown) => (v != null && v !== '' && v !== 'null') ? Number(v) : null;
    const data = { ...raw, supervisor: toNullableInt(raw.supervisor) };
    const req = this.isEditing
      ? this.api.updateEmployee(this.id!, data)
      : this.api.createEmployee(data);
    req.subscribe({
      next: () => { this.toast.show(this.isEditing ? 'Employee updated.' : 'Employee created.'); this.router.navigate(['/employees']); },
      error: err => (this.error = JSON.stringify(err.error)),
    });
  }
}

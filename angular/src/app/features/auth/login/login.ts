import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './login.html',
})
export class LoginComponent {

  form: FormGroup;
  error = '';

  constructor(
    private fb: FormBuilder,
    private auth: AuthService,
    private router: Router,
    private route: ActivatedRoute,
  ) {
    if (this.auth.isLoggedIn()) {
      this.router.navigate(['/']);
    }
    this.form = this.fb.group({
      enumber: ['', Validators.required],
      password: ['', Validators.required],
    });
  }

  submit(): void {
    if (this.form.invalid) return;
    const { enumber, password } = this.form.value;
    this.auth.login(+enumber, password).subscribe({
      next: () => {
        this.auth.getCurrentUser(true).subscribe(() => {
          const next = this.route.snapshot.queryParamMap.get('next');
          this.router.navigateByUrl(next && next.startsWith('/') ? next : '/');
        });
      },
      error: () => (this.error = 'Invalid employee number or password.'),
    });
  }
}

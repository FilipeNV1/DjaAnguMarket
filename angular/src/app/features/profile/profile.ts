import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { DecimalPipe } from '@angular/common';
import { AuthService } from '../../core/services/auth.service';
import { Me } from '../../core/models';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink, DecimalPipe],
  templateUrl: './profile.html',
})
export class ProfileComponent implements OnInit {
  user: Me | null = null;
  form: FormGroup;
  error = '';
  success = '';
  saving = false;
  showPasswordForm = false;

  constructor(private auth: AuthService, private fb: FormBuilder) {
    this.form = this.fb.group({
      old_password: ['', Validators.required],
      new_password: ['', [Validators.required, Validators.minLength(8)]],
      confirm_password: ['', Validators.required],
    });
  }

  ngOnInit(): void {
    this.auth.getCurrentUser(true).subscribe(u => (this.user = u));
  }

  togglePasswordForm(): void {
    this.showPasswordForm = !this.showPasswordForm;
    this.error = '';
    this.success = '';
    this.form.reset();
  }

  submit(): void {
    this.error = '';
    this.success = '';
    if (this.form.invalid) return;

    const { old_password, new_password, confirm_password } = this.form.value;
    if (new_password !== confirm_password) {
      this.error = 'New password and confirmation do not match.';
      return;
    }

    this.saving = true;
    this.auth.changePassword(old_password, new_password).subscribe({
      next: res => {
        this.success = res.detail;
        this.saving = false;
        this.form.reset();
        this.showPasswordForm = false;
      },
      error: err => {
        this.error = this.parseError(err.error);
        this.saving = false;
      },
    });
  }

  private parseError(e: unknown): string {
    if (!e) return 'Could not change password.';
    if (typeof e === 'string') return e;
    const obj = e as Record<string, string[] | string>;
    if (obj['old_password']) return ([] as string[]).concat(obj['old_password']).join(' ');
    if (obj['new_password']) return ([] as string[]).concat(obj['new_password']).join(' ');
    if (obj['detail']) return String(obj['detail']);
    return JSON.stringify(e);
  }
}

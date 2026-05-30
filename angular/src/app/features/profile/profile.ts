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
  profileForm: FormGroup;
  error = '';
  profileError = '';
  success = '';
  saving = false;
  savingProfile = false;
  showPasswordForm = false;
  showProfileForm = false;

  constructor(private auth: AuthService, private fb: FormBuilder) {
    this.form = this.fb.group({
      old_password: ['', Validators.required],
      new_password: ['', [Validators.required, Validators.minLength(8)]],
      confirm_password: ['', Validators.required],
    });
    this.profileForm = this.fb.group({
      name: ['', [Validators.required, Validators.maxLength(64)]],
      contact: ['', [Validators.required, Validators.maxLength(64)]],
      age: [null, [Validators.required, Validators.min(16)]],
      sex: ['', Validators.required],
    });
  }

  ngOnInit(): void {
    this.auth.getCurrentUser(true).subscribe(u => (this.user = u));
  }

  togglePasswordForm(): void {
    this.showPasswordForm = !this.showPasswordForm;
    this.showProfileForm = false;
    this.clearMessages();
    this.form.reset();
  }

  toggleProfileForm(): void {
    this.showProfileForm = !this.showProfileForm;
    this.showPasswordForm = false;
    this.clearMessages();
    if (this.showProfileForm && this.user) {
      this.profileForm.patchValue({
        name: this.user.name,
        contact: this.user.contact ?? '',
        age: this.user.age ?? null,
        sex: this.user.sex ?? '',
      });
    }
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

  saveProfile(): void {
    this.profileError = '';
    this.success = '';
    if (this.profileForm.invalid) return;

    this.savingProfile = true;
    this.auth.updateProfile(this.profileForm.value).subscribe({
      next: u => {
        this.user = u;
        this.savingProfile = false;
        this.showProfileForm = false;
        this.success = 'Profile updated successfully.';
      },
      error: err => {
        this.profileError = this.parseError(err.error);
        this.savingProfile = false;
      },
    });
  }

  private clearMessages(): void {
    this.error = '';
    this.profileError = '';
    this.success = '';
  }

  private parseError(e: unknown): string {
    if (!e) return 'Something went wrong.';
    if (typeof e === 'string') return e;
    const obj = e as Record<string, unknown>;
    if (obj['detail']) return String(obj['detail']);
    const parts = Object.values(obj).map(v => (Array.isArray(v) ? v.join(' ') : String(v)));
    return parts.length ? parts.join(' ') : JSON.stringify(e);
  }
}

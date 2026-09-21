import { Component, inject } from '@angular/core';
import {
  FormBuilder,
  ReactiveFormsModule,
  Validators
} from '@angular/forms';

import { ContactService } from '../../services/contact.service';

@Component({
  selector: 'app-contact',
  imports: [ReactiveFormsModule],
  templateUrl: './contact.html',
  styleUrl: './contact.scss'
})
export class Contact {

  private fb = inject(FormBuilder);
  private contactService = inject(ContactService);

  contactForm = this.fb.nonNullable.group({
    name: ['', [
      Validators.required,
      Validators.minLength(2)
    ]],

    email: ['', [
      Validators.required,
      Validators.email
    ]],

    message: ['', [
      Validators.required,
      Validators.minLength(10)
    ]]
  });

  isSubmitting = false;
  successMessage = '';
  errorMessage = '';

  onSubmit(): void {
    this.successMessage = '';
    this.errorMessage = '';

    if (this.contactForm.invalid) {
      this.contactForm.markAllAsTouched();
      return;
    }

    this.isSubmitting = true;

    const formData = this.contactForm.getRawValue();

    this.contactService.sendMessage(formData).subscribe({
      next: (response) => {
        this.successMessage = response.message;
        this.contactForm.reset();
        this.isSubmitting = false;
      },

      error: () => {
        this.errorMessage =
          'Something went wrong. Please try again later.';
        this.isSubmitting = false;
      }
    });
  }
}
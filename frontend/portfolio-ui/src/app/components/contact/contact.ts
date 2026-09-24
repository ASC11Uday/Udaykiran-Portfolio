import { Component, inject } from '@angular/core';
import {
  FormBuilder,
  ReactiveFormsModule,
  Validators
} from '@angular/forms';

import { ContactService } from '../../services/contact.service';
import { ScrollRevealDirective } from '../../shared/scroll-reveal.directive';

@Component({
  selector: 'app-contact',
  imports: [ReactiveFormsModule,ScrollRevealDirective],
  templateUrl: './contact.html',
  styleUrl: './contact.scss'
})
export class Contact {

  private fb = inject(FormBuilder);

  private contactService =
    inject(ContactService);


  contactForm =
    this.fb.nonNullable.group({

      name: [
        '',
        [
          Validators.required,
          Validators.minLength(2)
        ]
      ],

      email: [
        '',
        [
          Validators.required,
          Validators.email
        ]
      ],

      message: [
        '',
        [
          Validators.required,
          Validators.minLength(10)
        ]
      ]

    });


  isSubmitting = false;

  isSent = false;

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


    const formData =
      this.contactForm.getRawValue();


    this.contactService
      .sendMessage(formData)
      .subscribe({

        next: (response) => {

          this.successMessage =
            response.message;

          this.isSubmitting = false;

          /*
           * Wait until the button finishes
           * its sending state, then flip the card.
           */
          setTimeout(() => {

            this.isSent = true;

            this.contactForm.reset();

          }, 450);

        },

        error: () => {

          this.errorMessage =
            'Something went wrong. Please try again later.';

          this.isSubmitting = false;

        }

      });

  }


  sendAnotherMessage(): void {

    this.isSent = false;

    this.successMessage = '';

    this.errorMessage = '';

    this.contactForm.reset();

  }

}
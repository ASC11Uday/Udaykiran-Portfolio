import {
  Component,
  OnInit,
  inject,
  signal
} from '@angular/core';

import {
  AboutData,
  AboutService
} from '../../services/about.service';

@Component({
  selector: 'app-about',
  imports: [],
  templateUrl: './about.html',
  styleUrl: './about.scss'
})
export class About implements OnInit {

  private aboutService = inject(AboutService);

  about = signal<AboutData | null>(null);

  isLoading = signal(true);

  errorMessage = signal('');

  ngOnInit(): void {
    this.loadAbout();
  }

  loadAbout(): void {

    this.isLoading.set(true);

    this.errorMessage.set('');

    this.aboutService.getAbout().subscribe({

      next: (data) => {

        console.log('About received:', data);

        this.about.set(data);

        this.isLoading.set(false);

      },

      error: (error) => {

        console.error('About API error:', error);

        this.errorMessage.set(
          'Unable to load about information.'
        );

        this.isLoading.set(false);

      }

    });
  }
}
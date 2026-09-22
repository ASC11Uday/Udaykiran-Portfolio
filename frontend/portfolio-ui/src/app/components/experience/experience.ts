import {
  Component,
  OnInit,
  inject,
  signal
} from '@angular/core';

import {
  ExperienceData,
  ExperienceService
} from '../../services/experience.service';

@Component({
  selector: 'app-experience',
  imports: [],
  templateUrl: './experience.html',
  styleUrl: './experience.scss'
})
export class Experience implements OnInit {

  private experienceService = inject(ExperienceService);

  experiences = signal<ExperienceData[]>([]);

  isLoading = signal(true);

  errorMessage = signal('');

  ngOnInit(): void {
    this.loadExperiences();
  }

  loadExperiences(): void {

    this.isLoading.set(true);

    this.errorMessage.set('');

    this.experienceService.getExperiences().subscribe({

      next: (data) => {

        console.log('Experiences received:', data);

        this.experiences.set(data);

        this.isLoading.set(false);

      },

      error: (error) => {

        console.error(
          'Experience API error:',
          error
        );

        this.errorMessage.set(
          'Unable to load experience information.'
        );

        this.isLoading.set(false);

      }

    });
  }
}
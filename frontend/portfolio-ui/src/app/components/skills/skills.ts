import {
  Component,
  OnInit,
  inject,
  signal
} from '@angular/core';

import {
  SkillGroup,
  SkillService
} from '../../services/skill.service';

@Component({
  selector: 'app-skills',
  imports: [],
  templateUrl: './skills.html',
  styleUrl: './skills.scss'
})
export class Skills implements OnInit {

  private skillService = inject(SkillService);

  skillGroups = signal<SkillGroup[]>([]);

  isLoading = signal(true);

  errorMessage = signal('');

  ngOnInit(): void {
    this.loadSkills();
  }

  loadSkills(): void {

    this.isLoading.set(true);

    this.errorMessage.set('');

    this.skillService.getSkillGroups().subscribe({

      next: (data) => {

        console.log('Skills received:', data);

        this.skillGroups.set(data);

        this.isLoading.set(false);

      },

      error: (error) => {

        console.error(
          'Skills API error:',
          error
        );

        this.errorMessage.set(
          'Unable to load skills information.'
        );

        this.isLoading.set(false);

      }

    });
  }
}
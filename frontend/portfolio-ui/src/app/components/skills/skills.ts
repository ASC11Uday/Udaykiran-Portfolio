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

import {
  ScrollRevealDirective
} from '../../shared/scroll-reveal.directive';


@Component({
  selector: 'app-skills',
  imports: [ScrollRevealDirective],
  templateUrl: './skills.html',
  styleUrl: './skills.scss'
})
export class Skills implements OnInit {

  private skillService =
    inject(SkillService);


  // =========================================
  // SKILL DATA
  // =========================================

  skillGroups =
    signal<SkillGroup[]>([]);

  isLoading =
    signal(true);

  errorMessage =
    signal('');


  // =========================================
  // INITIALIZATION
  // =========================================

  ngOnInit(): void {

    this.loadSkills();

  }


  // =========================================
  // LOAD SKILLS
  // =========================================

  loadSkills(): void {

    this.isLoading.set(true);

    this.errorMessage.set('');


    this.skillService
      .getSkillGroups()
      .subscribe({

        next: (data) => {

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


  // =========================================
  // SKILL CARD ENTER
  // =========================================

  onSkillGroupEnter(
    card: HTMLElement
  ): void {

    card.classList.add(
      'is-active'
    );

  }


  // =========================================
  // SKILL CARD MOVE
  // =========================================

  onSkillGroupMove(
    event: MouseEvent,
    card: HTMLElement
  ): void {

    const rect =
      card.getBoundingClientRect();


    const x =
      event.clientX - rect.left;


    const y =
      event.clientY - rect.top;


    card.style.setProperty(
      '--mouse-x',
      `${x}px`
    );


    card.style.setProperty(
      '--mouse-y',
      `${y}px`
    );

  }


  // =========================================
  // SKILL CARD LEAVE
  // =========================================

  onSkillGroupLeave(
    card: HTMLElement
  ): void {

    card.classList.remove(
      'is-active'
    );


    card.style.removeProperty(
      '--mouse-x'
    );


    card.style.removeProperty(
      '--mouse-y'
    );

  }

}
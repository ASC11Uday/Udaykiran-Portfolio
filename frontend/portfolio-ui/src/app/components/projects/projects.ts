import {
  Component,
  OnInit,
  inject,
  signal
} from '@angular/core';

import {
  Project,
  ProjectService
} from '../../services/project.service';

import {
  ScrollRevealDirective
} from '../../shared/scroll-reveal.directive';


@Component({
  selector: 'app-projects',
  imports: [ScrollRevealDirective],
  templateUrl: './projects.html',
  styleUrl: './projects.scss'
})
export class Projects implements OnInit {

  private projectService =
    inject(ProjectService);


  // =========================================
  // PROJECT DATA
  // =========================================

  projects =
    signal<Project[]>([]);

  isLoading =
    signal(true);

  errorMessage =
    signal('');


  // =========================================
  // FLIP STATE
  // =========================================

  flippedProjectId =
    signal<number | null>(null);


  // =========================================
  // INITIALIZATION
  // =========================================

  ngOnInit(): void {

    this.loadProjects();

  }


  // =========================================
  // LOAD PROJECTS
  // =========================================

  loadProjects(): void {

    this.isLoading.set(true);

    this.errorMessage.set('');


    this.projectService
      .getProjects()
      .subscribe({

        next: (data) => {

          this.projects.set(data);

          this.isLoading.set(false);

        },


        error: (error) => {

          console.error(
            'Projects API error:',
            error
          );

          this.isLoading.set(false);

          this.errorMessage.set(
            'Unable to load projects. Please try again.'
          );

        }

      });

  }


  // =========================================
  // PROJECT CARD TILT
  // =========================================

  onCardMove(
    event: MouseEvent,
    card: HTMLElement
  ): void {

    /*
     * Once flipped, the card should
     * remain completely flat.
     */

    if (
      card.classList.contains(
        'is-flipped'
      )
    ) {

      return;

    }


    const rect =
      card.getBoundingClientRect();


    const x =
      event.clientX - rect.left;


    const y =
      event.clientY - rect.top;


    const centerX =
      rect.width / 2;


    const centerY =
      rect.height / 2;


    const rotateX =
      ((y - centerY) / centerY) * -4;


    const rotateY =
      ((x - centerX) / centerX) * 4;


    card.style.transform =
      `perspective(1000px)
       rotateX(${rotateX}deg)
       rotateY(${rotateY}deg)
       translateY(-4px)`;


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
  // PROJECT CARD LEAVE
  // =========================================

  onCardLeave(
    card: HTMLElement
  ): void {

    /*
     * Remove inline tilt.
     *
     * CSS will then decide whether
     * the card is normal or flipped.
     */

    card.style.transform = '';

    card.style.removeProperty(
      '--mouse-x'
    );

    card.style.removeProperty(
      '--mouse-y'
    );

  }


  // =========================================
  // TOGGLE PROJECT CARD
  // =========================================

  toggleProjectCard(
    projectId: number
  ): void {

    const card =
      document.querySelector(
        `.project-card[data-project-id="${projectId}"]`
      ) as HTMLElement | null;


    /*
     * Always remove the mouse tilt
     * BEFORE changing the flip state.
     */

    if (card) {

      card.style.transform = '';

      card.style.removeProperty(
        '--mouse-x'
      );

      card.style.removeProperty(
        '--mouse-y'
      );

    }


    const isCurrentlyFlipped =
      this.flippedProjectId() === projectId;


    /*
     * Same card:
     *     flipped -> normal
     *
     * Different card:
     *     old card closes
     *     new card opens
     */

    this.flippedProjectId.set(
      isCurrentlyFlipped
        ? null
        : projectId
    );

  }


  // =========================================
  // CHECK FLIP STATE
  // =========================================

  isProjectFlipped(
    projectId: number
  ): boolean {

    return (
      this.flippedProjectId() === projectId
    );

  }

}
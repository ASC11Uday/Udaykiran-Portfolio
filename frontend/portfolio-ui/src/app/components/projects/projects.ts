import { Component, OnInit, inject, signal } from '@angular/core';

import {
  Project,
  ProjectService
} from '../../services/project.service';

@Component({
  selector: 'app-projects',
  imports: [],
  templateUrl: './projects.html',
  styleUrl: './projects.scss'
})
export class Projects implements OnInit {

  private projectService = inject(ProjectService);

  projects = signal<Project[]>([]);

  isLoading = signal(true);

  errorMessage = signal('');

  ngOnInit(): void {
    this.loadProjects();
  }

  loadProjects(): void {

    this.isLoading.set(true);
    this.errorMessage.set('');

    this.projectService.getProjects().subscribe({

      next: (data) => {

        console.log('Projects received:', data);

        this.projects.set(data);

        this.isLoading.set(false);

      },

      error: (error) => {

        console.error('Projects API error:', error);

        this.isLoading.set(false);

        this.errorMessage.set(
          'Unable to load projects. Please try again.'
        );

      }

    });
  }
}
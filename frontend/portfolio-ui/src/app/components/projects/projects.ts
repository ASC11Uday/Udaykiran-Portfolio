import { Component, OnInit, inject } from '@angular/core';

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

  projects: Project[] = [];

  isLoading = true;
  errorMessage = '';

  ngOnInit(): void {
    this.loadProjects();
  }

  loadProjects(): void {

  console.log('Loading projects...');

  this.projectService.getProjects().subscribe({

    next: (data) => {

      console.log('Projects received:', data);

      this.projects = data;
      this.isLoading = false;
    },

    error: (error) => {

      console.error('Projects API error:', error);

      this.errorMessage =
        'Unable to load projects right now.';

      this.isLoading = false;
    }

  });
}
}
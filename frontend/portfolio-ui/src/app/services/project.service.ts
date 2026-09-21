import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';

export interface Project {
  id: number;
  title: string;
  description: string;
  type: string;
  category: string;
  technologies: string[];
  github: string;
  featured: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class ProjectService {

  private http = inject(HttpClient);

  private apiUrl = environment.apiUrl;

  getProjects(): Observable<Project[]> {
    return this.http.get<Project[]>(
      `${this.apiUrl}/projects`
    );
  }
}
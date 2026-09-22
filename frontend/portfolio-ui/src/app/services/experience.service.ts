import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';

export interface ExperienceData {
  id: number;
  role: string;
  company: string;
  period: string;
  description: string;
  technologies: string[];
}

@Injectable({
  providedIn: 'root'
})
export class ExperienceService {

  private http = inject(HttpClient);

  private apiUrl = environment.apiUrl;

  getExperiences(): Observable<ExperienceData[]> {
    return this.http.get<ExperienceData[]>(
      `${this.apiUrl}/experiences`
    );
  }
}
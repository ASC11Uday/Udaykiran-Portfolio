import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';

export interface SkillGroup {
  id: number;
  title: string;
  description: string;
  skills: string[];
}

@Injectable({
  providedIn: 'root'
})
export class SkillService {

  private http = inject(HttpClient);

  private apiUrl = environment.apiUrl;

  getSkillGroups(): Observable<SkillGroup[]> {
    return this.http.get<SkillGroup[]>(
      `${this.apiUrl}/skills`
    );
  }
}
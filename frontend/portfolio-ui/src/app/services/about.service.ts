import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';

export interface AboutData {
  name: string;
  role: string;
  skills: string[];
}

@Injectable({
  providedIn: 'root'
})
export class AboutService {

  private http = inject(HttpClient);

  private apiUrl = environment.apiUrl;

  getAbout(): Observable<AboutData> {
    return this.http.get<AboutData>(
      `${this.apiUrl}/about`
    );
  }
}
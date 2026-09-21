import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface ContactRequest {
  name: string;
  email: string;
  message: string;
}

export interface ContactResponse {
  message: string;
}

@Injectable({
  providedIn: 'root'
})
export class ContactService {

  private http = inject(HttpClient);

  private apiUrl = environment.apiUrl;

  sendMessage(data: ContactRequest): Observable<ContactResponse> {
    return this.http.post<ContactResponse>(
      `${this.apiUrl}/contact`,
      data
    );
  }
}
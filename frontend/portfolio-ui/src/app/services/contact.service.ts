import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

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

  private apiUrl = 'http://127.0.0.1:8000/api';

  sendMessage(data: ContactRequest): Observable<ContactResponse> {
    return this.http.post<ContactResponse>(
      `${this.apiUrl}/contact`,
      data
    );
  }
}
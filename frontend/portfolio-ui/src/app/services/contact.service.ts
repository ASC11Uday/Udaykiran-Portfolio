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
  success: boolean;
  message: string;
}

@Injectable({
  providedIn: 'root'
})
export class ContactService {

  private http = inject(HttpClient);

  private web3FormsUrl = 'https://api.web3forms.com/submit';

  sendMessage(data: ContactRequest): Observable<ContactResponse> {

    const formData = {
      access_key: environment.web3FormsAccessKey,
      name: data.name,
      email: data.email,
      message: data.message,
      subject: `New Portfolio Contact from ${data.name}`,
      from_name: 'Udaykiran Portfolio',
      replyto: data.email
    };

    return this.http.post<ContactResponse>(
      this.web3FormsUrl,
      formData
    );
  }
}
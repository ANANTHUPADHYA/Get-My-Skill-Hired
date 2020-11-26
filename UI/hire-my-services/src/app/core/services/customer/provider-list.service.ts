import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { ProviderDetailsResponse } from './index';
import { Observable } from 'rxjs';
import { urlConstants } from '../../rest-api-configuration';
import { BookAppointmentReq, BookAppointmentResp } from './models';

@Injectable({
  providedIn: 'root'
})
export class ProviderListService {
  private baseUrl: string;
  constructor(private http: HttpClient) { 
    this.baseUrl = environment.url;
  }
  getListOfProviders(serviceName): Observable<ProviderDetailsResponse> {
    // return this.http.get<ProviderDetailsResponse>(`${this.baseUrl}${urlConstants.GET_PROVIDERS}/${serviceName}`); 
    return this.http.get<ProviderDetailsResponse>('http://localhost:3000/providers');
  }

  scheduleAppointment(params: BookAppointmentReq):Observable<BookAppointmentResp> {
     // return this.http.post<ProviderDetailsResponse>(`${this.baseUrl}${urlConstants.BOOK_APPNT}`, params); 
     return this.http.get<BookAppointmentResp>('http://localhost:3000/book')
  }
  
}
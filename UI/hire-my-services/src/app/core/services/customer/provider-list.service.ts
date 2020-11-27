import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { ProviderDetailsResponse } from './index';
import { Observable } from 'rxjs';
import { urlConstants } from '../../rest-api-configuration';
import { AppointmentList, BookAppointmentReq, BookAppointmentResp, ChangeStatusParams, ChangeStatusResponse, ReviewParams } from './models';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ProviderListService {
  private baseUrl: string;
  constructor(private http: HttpClient) { 
    this.baseUrl = environment.url;
  }
  getListOfProviders(serviceName: string): Observable<ProviderDetailsResponse> {
    const name = serviceName.toLowerCase();
    return this.http.get<ProviderDetailsResponse>(`${this.baseUrl}${urlConstants.GET_PROVIDERS}?skillSet=${name}`); 
    // return this.http.get<ProviderDetailsResponse>('http://localhost:3000/providers');
  }

  scheduleAppointment(params: BookAppointmentReq):Observable<BookAppointmentResp> {
     // return this.http.post<ProviderDetailsResponse>(`${this.baseUrl}${urlConstants.BOOK_APPNT}`, params); 
     return this.http.get<BookAppointmentResp>('http://localhost:3000/book')
  }

  getListOfAppointments(uuid: string):Observable<AppointmentList> {
    return this.http.get<AppointmentList>('http://localhost:3000/appointments');
    // return this.http.get<AppointmentList>(`${this.baseUrl}${urlConstants.GET_APPOINTMENTS}/${uuid}`);
  }


  changeApptStatus(changeStatusParams: ChangeStatusParams):Observable<ChangeStatusResponse>{
    return this.http.post<ChangeStatusResponse>(`${this.baseUrl}/user/${changeStatusParams.uuid}/appointments/${changeStatusParams.appId}`, {status: changeStatusParams.status});
  }

  postReview(reviewParams: ReviewParams): Observable<ChangeStatusResponse> {
    return this.http.post<ChangeStatusResponse>(`${this.baseUrl}/user/${reviewParams.uuid}/appointments/${reviewParams.appId}`, {review: reviewParams.review, rating: reviewParams.rating});

  }
}

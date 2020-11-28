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
    return this.http.get<ProviderDetailsResponse>(`${this.baseUrl}${urlConstants.GET_PROVIDERS}?skillSet=${serviceName}`); 
  }

  scheduleAppointment(params: BookAppointmentReq, uuid: string):Observable<BookAppointmentResp> {
     return this.http.post<BookAppointmentResp>(`${this.baseUrl}/users/${uuid}/appointments`, params); 
  }

  getListOfAppointments(uuid: string):Observable<AppointmentList> {
    return this.http.get<AppointmentList>(`${this.baseUrl}/users/${uuid}/customerAppointments`);
  }


  changeApptStatus(changeStatusParams: ChangeStatusParams, uuid: string):Observable<ChangeStatusResponse>{
    const params =  {status: changeStatusParams.status}
    return this.http.patch<ChangeStatusResponse>(`${this.baseUrl}/users/${uuid}/appointments/${changeStatusParams.appId}`, params);
  }

  postReview(reviewParams: ReviewParams): Observable<ChangeStatusResponse> {
    return this.http.patch<ChangeStatusResponse>(`${this.baseUrl}/users/${reviewParams.uuid}/appointments/${reviewParams.appId}/ratingAndReview`, {review: reviewParams.review, rating: reviewParams.rating});

  }
}

import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { AppointmentList, ChangeStatusParams, ChangeStatusResponse } from '..';

@Injectable({
  providedIn: 'root'
})
export class ProviderService {

  private baseUrl: string;
  constructor(private http: HttpClient) { 
    this.baseUrl = environment.url;
  }

  getListOfAppointments(uuid: string):Observable<AppointmentList> {
    return this.http.get<AppointmentList>(`${this.baseUrl}/users/${uuid}/providerAppointments`);
  }

  changeApptStatus(changeStatusParams: ChangeStatusParams):Observable<ChangeStatusResponse>{
    const params =  {status: changeStatusParams.status}
    return this.http.patch<ChangeStatusResponse>(`${this.baseUrl}/users/${changeStatusParams.uuid}/appointments/${changeStatusParams.appId}`, params);
  }

}

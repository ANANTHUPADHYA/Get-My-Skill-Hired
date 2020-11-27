import { environment } from 'src/environments/environment';
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { LoginResponse, UserParams, RegisterResponse } from './models';
import { Observable, of, Subject } from 'rxjs';
import { urlConstants } from '../../rest-api-configuration';

@Injectable({
  providedIn: 'root'
})
export class LoginService {
  private baseUrl: string;
  constructor(private http: HttpClient) { 
    this.baseUrl = environment.url;
  }

  loginUser({email, password}): Observable<LoginResponse> {
    const httpHeaders: HttpHeaders = new HttpHeaders({
      Authorization: `Basic ${window.btoa(email + ':' + password)}`
  });
    return this.http.get<LoginResponse>(`${this.baseUrl}${urlConstants.LOGIN}`,{headers: httpHeaders});
    // return this.http.get<LoginResponse>('http://localhost:3000/login');
  }


  registerUser(userDetails: UserParams, password:string, email:string):  Observable<RegisterResponse> {
    const httpHeaders: HttpHeaders = new HttpHeaders({
      Authorization: `Basic ${window.btoa(email + ':' + password)}`
  });
    return this.http.post<RegisterResponse>(`${this.baseUrl}${urlConstants.REGISTER}`, userDetails, {headers: httpHeaders}); 
    // return this.http.get<RegisterResponse>('http://localhost:3000/register');
  }

  logout():Observable<any> {
    return this.http.get(`${this.baseUrl}${urlConstants.LOGOUT}`);
  }
}

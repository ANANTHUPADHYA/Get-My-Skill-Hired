import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { UserProfileResponse, UploadImageResponse } from './models';
import { Observable } from 'rxjs';
import { urlConstants } from '../../rest-api-configuration';
import { UserParams, RegisterResponse } from '..';

@Injectable({
  providedIn: 'root'
})
export class ProfileService {
  private baseUrl: string;
  constructor(private http: HttpClient) { 
    this.baseUrl = environment.url;
  }

  uploadImage(fileToUpload: File, email: string): Observable<UploadImageResponse> {
    const formData: FormData = new FormData();
    formData.append('profile_image', fileToUpload, fileToUpload.name);
    return this.http.put<UploadImageResponse>(`${this.baseUrl}${urlConstants.IMAGE_UPLOAD}`, formData);
  }
  updateProfile(userDetails: UserParams, userType: string):  Observable<RegisterResponse> {
    return this.http.put<RegisterResponse>(`${this.baseUrl}${urlConstants.UPDATE_PROFILE}/${userType}`, userDetails); 
  }
}

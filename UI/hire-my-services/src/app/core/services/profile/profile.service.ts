import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { UserProfileResponse, UploadImageResponse } from './models';
import { Observable } from 'rxjs';
import { urlConstants } from '../../rest-api-configuration';

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
    formData.append('file', fileToUpload, fileToUpload.name);
    return this.http.post<UploadImageResponse>(`${this.baseUrl}${urlConstants.IMAGE_UPLOAD}/${email}`, formData);
  }
}

import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor
} from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable()
export class AppHttpInterceptor implements HttpInterceptor {

  constructor() {}

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
   // Get the auth token from the session.
   const authToken = sessionStorage.getItem('sessionID');

   // Clone the request and replace the original headers with
   // cloned headers, updated with the authorization.
   if (authToken) {
   const authReq = request.clone({
     headers: request.headers.set('Authorization',  `Bearer ${authToken}`)
   });
    // send cloned request with header to the next handler.
   return next.handle(authReq);
 }

   return next.handle(request);
  }
}

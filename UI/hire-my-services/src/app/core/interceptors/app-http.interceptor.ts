import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpResponse
} from '@angular/common/http';
import { Observable } from 'rxjs';
import { SharedService } from '../services';
import {catchError, map} from 'rxjs/operators'

@Injectable()
export class AppHttpInterceptor implements HttpInterceptor {
  constructor(private sharedService: SharedService) {}

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {

    this.sharedService.showSppiner.next(true);
   // Get the auth token from the session.
   const authToken = sessionStorage.getItem('sessionID');


   // Clone the request and replace the original headers with
   // cloned headers, updated with the authorization.
   if (authToken && !request.url.includes('signin')) {
   const authReq = request.clone({
     headers: request.headers.set('Authorization',  `Bearer ${authToken}`)
   });
    // send cloned request with header to the next handler.
   return next.handle(authReq).pipe(catchError((err) => {
    this.sharedService.showSppiner.next(false);
    return err;
  }))
  .pipe(map<HttpEvent<any>, any>((evt: HttpEvent<any>) => {
    if (evt instanceof HttpResponse) {
      this.sharedService.showSppiner.next(false);
    }
    return evt;
  }));
 }

   return next.handle(request).pipe(catchError((err) => {
    this.sharedService.showSppiner.next(false);
    return err;
  }))
  .pipe(map<HttpEvent<any>, any>((evt: HttpEvent<any>) => {
    if (evt instanceof HttpResponse) {
      this.sharedService.showSppiner.next(false);
    }
    return evt;
  }));;
  }
}

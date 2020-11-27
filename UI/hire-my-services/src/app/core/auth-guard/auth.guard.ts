import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, UrlTree, Router } from '@angular/router';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
  constructor(private router: Router) {}
  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {

      const url: string = state.url;
      const loggedIn = this.checkLogin(url);
      if (loggedIn) {
        return true;
      } else {
        this.router.navigate(['/login']);
      }
  }

  checkLogin(url: string): boolean {
    const token = sessionStorage.getItem('sessionID');
    if (token) {
      return true;
    } else {
      return false;
    }

    // Redirect to the login page
  }
  
}

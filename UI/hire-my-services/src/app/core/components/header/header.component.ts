import { Router } from '@angular/router';
import { LoginService } from '../../../core/services';
import { Subscription } from 'rxjs';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { SharedService } from '../../services/shared';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit, OnDestroy {
  private subscriptions = new Subscription();
  public cartItems: number;
  public userEmail: string;
  public showLogIn: boolean = false;
  public usertype: string;
  constructor(
    private router: Router,
    private snackBar: MatSnackBar,
    private sharedService: SharedService,
    private loginService: LoginService
  ) {}

  ngOnInit() {

    this.usertype = sessionStorage.getItem('usertype');
    if (sessionStorage.getItem('sessionID')) {
      this.showLogIn = true;
    } else {
      this.showLogIn = false;
    }
    this.subscriptions.add(
      this.sharedService.userLoggedIn.subscribe(isLoggedIn => {
          this.showLogIn = isLoggedIn;
      })
    );
    
  }

  initializeUser() {
   
    this.userEmail = sessionStorage.getItem('email');
    // this.getUserData();
  }

  openSnackBar(message: string, className: string) {
    this.snackBar.open(message, '', {
      duration: 5000,
      panelClass: ['mat-toolbar', className]
    });
  }


  /* getUserData() {
    this.subscriptions.add(
      this.userService.getUserDetails(this.userEmail).subscribe(response => {
        if (response.success) {
          this.userData = response.data;
          sessionStorage.setItem('userData', JSON.stringify(response.data));
        }
      },
      error => {
        this.openSnackBar(error.error.error, 'mat-warn');
      })
    );
  } */

  logout() {
          this.loginService.logout().subscribe(data => {
            sessionStorage.clear();
          this.router.navigate(['login']);
          this.showLogIn = false;
          });
  }


  goToCart() {
    this.router.navigate(['/cart']);
  }
  goToAdmin() {
    this.router.navigate(['/admin']);
  }
  ngOnDestroy() {
    this.subscriptions.unsubscribe();
  }

  goToHome() {
    if(this.usertype === 'consumer') {
      this.router.navigate(['customer']);
    } else {
      this.router.navigate(['provider']);
    }
  }
}

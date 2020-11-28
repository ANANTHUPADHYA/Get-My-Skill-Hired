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


  openSnackBar(message: string, className: string) {
    this.snackBar.open(message, '', {
      duration: 5000,
      panelClass: ['mat-toolbar', className]
    });
  }


  logout() {
          this.loginService.logout().subscribe(data => {
            sessionStorage.clear();
          this.router.navigate(['login']);
          this.showLogIn = false;
          });
  }


  goToAppointment() {
    this.router.navigate(['customer/appointments']);
  }

  goToHome() {
    if(this.usertype === 'consumer') {
      this.router.navigate(['customer']);
    } else {
      this.router.navigate(['provider']);
    }
  }

  goToProfile() {
    if(this.usertype === 'consumer') {
      this.router.navigate(['customer/profile']);
    } else {
      this.router.navigate(['provider/profile']);
    }
  }

  ngOnDestroy() {
    this.subscriptions.unsubscribe();
  }
}

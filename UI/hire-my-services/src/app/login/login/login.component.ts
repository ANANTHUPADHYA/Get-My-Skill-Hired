import { MatSnackBar } from '@angular/material/snack-bar';
import { LoginService } from '../../core/services';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Subscription } from 'rxjs';
import { Router } from '@angular/router';
import { SharedService } from 'src/app/core/services/shared';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit, OnDestroy {
  public loginForm: FormGroup;
  private subscriptions = new Subscription();
  constructor(private formBuilder: FormBuilder, private loginService: LoginService, private router: Router, private snackBar: MatSnackBar, private sharedService: SharedService) {
   this.loginForm = this.formBuilder.group({
      email: ['', Validators.email],
      password: ['', Validators.required]
    });
   }
  ngOnInit() {
    const token = sessionStorage.getItem('token');
    if(token) {
      this.sharedService.userLoggedIn.next(true);
      const usertype = sessionStorage.getItem('usertype');
      if(usertype === 'consumer') {
        this.router.navigate(['customer']);
      } else {
        this.router.navigate(['provider']);
      }
    }
  }

  openSnackBar(message: string, className: string) {
    this.snackBar.open(message, '', {
      duration: 5000,
      panelClass: ['mat-toolbar', className]
    });
  }


  onSubmit() {
    console.log('value', this.loginForm.value);
    this.subscriptions.add(this.loginService.loginUser(this.loginForm.value).subscribe(response => {
      if (response.success && response.data) {
       sessionStorage.setItem('email', this.loginForm.value.email);
       sessionStorage.setItem('sessionID', response.data.idToken);
       sessionStorage.setItem('usertype', response.data.profile.usertype);
       sessionStorage.setItem('profile', JSON.stringify(response.data.profile))
       this.sharedService.userLoggedIn.next(true);
       if(response.data.profile.usertype === 'consumer') {
        this.router.navigate(['/customer']);
       } else {
         this.router.navigate(['/provider'])
       }
       
      }
    }, error => {
      this.openSnackBar(error.error.data, 'mat-warn');
    }));
  }

  ngOnDestroy() {
    this.subscriptions.unsubscribe();
  }

  goToRegister() {
    this.router.navigate(['login/register']);
  }
}

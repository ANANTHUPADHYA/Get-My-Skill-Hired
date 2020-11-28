import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ProfileService, UserParams } from 'src/app/core/services';

@Component({
  selector: 'app-customer-profile',
  templateUrl: './customer-profile.component.html',
  styleUrls: ['./customer-profile.component.scss']
})
export class CustomerProfileComponent implements OnInit {
  public signupFormCustomer: FormGroup;
  public userProfile;
  public isDisabled = true;

  constructor(private formBuilder: FormBuilder, private profileService: ProfileService, private snackBar: MatSnackBar) { 
    
  }
  ngOnInit(): void {
    this.userProfile = JSON.parse(sessionStorage.getItem('profile'));
    this.initializeForm();
  }
  initializeForm() {
    this.signupFormCustomer = this.formBuilder.group({
      email: [this.userProfile.email, Validators.email],
      firstName: [this.userProfile.firstName, Validators.required],
      lastName: [this.userProfile.lastName, Validators.required],
      address: [this.userProfile.address, Validators.required],
      area: [this.userProfile.area, Validators.required],
      city: [this.userProfile.city, Validators.required],
      phone: [parseInt(this.userProfile.phone.substring(2)), Validators.required],
    });
    this.signupFormCustomer.disable();
  }

  edit() {
    this.signupFormCustomer.enable();
    this.signupFormCustomer.controls.email.disable()
  }



  profileDetailsSet() {
    this.userProfile.email = this.signupFormCustomer.controls.email.value;
    this.userProfile.firstName = this.signupFormCustomer.controls.firstName.value;
    this.userProfile.lastName = this.signupFormCustomer.controls.lastName.value;
    this.userProfile.address = this.signupFormCustomer.controls.address.value;
    this.userProfile.area = this.signupFormCustomer.controls.area.value;
    this.userProfile.city = this.signupFormCustomer.controls.city.value;
    this.userProfile.phone = "+91"  + this.signupFormCustomer.controls.phone.value.toString();
    sessionStorage.setItem('profile', JSON.stringify(this.userProfile));

  }

  register() {
  let formValue:UserParams;
    formValue = this.signupFormCustomer.value;
    delete formValue['password'];
    formValue['phone']= "+91" + formValue['phone'].toString();
    delete formValue['email'];
    const userType = this.userProfile.userType;
    this.profileService.updateProfile(formValue, userType).subscribe(response => {
      if (response.success) {
                this.openSnackBar('Profile Updated', 'mat-primary')
        this.isDisabled = true;
        this.profileDetailsSet();
      }
    },  error => {
      this.openSnackBar(error.error.data, 'mat-warn');
    });
  }

  openSnackBar(message: string, className: string) {
    this.snackBar.open(message, '', {
      duration: 5000,
      panelClass: ['mat-toolbar', className]
    });
  }


}

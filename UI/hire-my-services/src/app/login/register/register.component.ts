import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators, FormControl } from '@angular/forms';
import { LoginService, UserParams, ProfileService } from 'src/app/core/services';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { servicesList, days, timings } from 'src/app/core/config';
import { element } from 'protractor';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {
  public userType: string;
  public signupFormCustomer: FormGroup;
  public signupFormProvider: FormGroup;
  public skillset = servicesList;
  public days = days;
  public timing = timings;
 public selectedDays = [];
  public toTimeArray = [];
  public selectedSkills = [];
  public showAddSkill = true;
  constructor(private formBuilder: FormBuilder, private loginService: LoginService, private snackBar: MatSnackBar, private router: Router,
    private profileService: ProfileService) {
    this.signupFormCustomer = this.formBuilder.group({
      email: ['', Validators.email],
      password: ['', Validators.required],
      firstName: ['', Validators.required],
      lastName: ['', Validators.required],
      address: ['', Validators.required],
      area: ['', Validators.required],
      city: ['', Validators.required],
      phone: ['', Validators.required],
      
    });
    this.signupFormProvider = this.formBuilder.group({
      email: ['', Validators.email],
      password: ['', Validators.required],
      firstName: ['', Validators.required],
      lastName: ['', Validators.required],
      address: ['', Validators.required],
      area: ['', Validators.required],
      city: ['', Validators.required],
      phone: ['', Validators.required],
      fromTime: ['', Validators.required],
      toTime: ['', Validators.required],
      selectedDays: [[], Validators.required]
    });
   }

  ngOnInit(): void {
    this.selectedSkills.push({
      name: '',
      price: 0
    })
  }

  register() {
    let formValue:UserParams;
    let password, email;
    if(this.userType === 'consumer') {
      formValue = this.signupFormCustomer.value;
      formValue['userType'] = 'consumer';
      password = this.signupFormCustomer.controls.password.value;
    } else {
      password = this.signupFormProvider.controls.password.value
      formValue = this.signupFormProvider.value;
      formValue['userType'] = 'provider';
      formValue.skillSet = this.selectedSkills;
      formValue.time = this.signupFormProvider.controls.fromTime.value + "-" + this.signupFormProvider.controls.toTime.value;
      formValue.days = this.signupFormProvider.controls.selectedDays.value;
      delete formValue['selectedDays'];
      delete formValue['fromTime'];
      delete formValue['toTime'];
    }
    console.log(formValue);
    delete formValue['password'];
    email = formValue['email'];
    formValue['phone']= "+91" + formValue['phone'].toString();
    delete formValue['email'];
    this.loginService.registerUser(formValue, password, email).subscribe(response => {
      if (response.success) {
        this.openSnackBar(response.data, 'mat-primary');
        this.router.navigate(['/login']);
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

  populateToTiming() {
    let time: number;
    this.toTimeArray = [];
    this.signupFormProvider.setControl('toTime', new FormControl('', Validators.required));
    const selectedIndex= this.timing.indexOf(this.signupFormProvider.controls.fromTime.value);
    this.timing.forEach((element,index) => {
      if(index > selectedIndex) {
        this.toTimeArray.push(element)
      }
    });
  }


  addSkill() {
    this.selectedSkills.push({
      name: '',
      price: 0
    });
    if(this.selectedSkills.length >= this.skillset.length) {
      this.showAddSkill = false
    } else {
      this.showAddSkill = true;
    }

  }

  removeSkill(index) {
    this.selectedSkills.splice(index,1);
    if(this.selectedSkills.length >= this.skillset.length) {
      this.showAddSkill = false
    } else {
      this.showAddSkill = true;
    }
  }

  checkPresent(skill) {
    const skills = this.selectedSkills.find(element => element.name === skill);
    if(skills) {
      return true;
    } else {
      return false;
    }
  }

  checkSkillSets() {
    const empty = this.selectedSkills.find(element => element.name === '')
    if(empty) {
      return true;
    } else {
      return false;
    }
  }

}

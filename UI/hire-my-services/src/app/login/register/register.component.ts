import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators, FormControl } from '@angular/forms';
import { LoginService, UserParams } from 'src/app/core/services';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { servicesList } from 'src/app/core/config';

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
  public days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
  public timing = ["9:00 AM", "10:00 AM", "11:00 AM","12:00 PM","1:00 PM","2:00 PM","3:00 PM","4:00 PM","5:00 PM","6:00 PM"];
 public selectedDays = [];
  public toTimeArray = [];
  public selectedSkills: string;
  constructor(private formBuilder: FormBuilder, private loginService: LoginService, private snackBar: MatSnackBar, private router: Router) {
    this.signupFormCustomer = this.formBuilder.group({
      email: ['', Validators.email],
      password: ['', Validators.required],
      firstname: ['', Validators.required],
      lastname: ['', Validators.required],
      address: ['', Validators.required],
      area: ['', Validators.required],
      city: ['', Validators.required],
      phone: ['', Validators.required],
      
    });
    this.signupFormProvider = this.formBuilder.group({
      email: ['', Validators.email],
      password: ['', Validators.required],
      firstname: ['', Validators.required],
      lastname: ['', Validators.required],
      address: ['', Validators.required],
      area: ['', Validators.required],
      city: ['', Validators.required],
      phone: ['', Validators.required],
      fromTime: ['', Validators.required],
      toTime: ['', Validators.required],
      selectedSkills: [[], Validators.required],
      selectedDays: [[], Validators.required],
      price: [0, Validators.required],
      image: [''],
    });
   }

  ngOnInit(): void {
  }

  register() {
    let formValue:UserParams;
    let password;
    if(this.userType === 'consumer') {
      formValue = this.signupFormCustomer.value;
      formValue['usertype'] = 'consumer';
      password = this.signupFormCustomer.controls.password.value;
    } else {
      password = this.signupFormProvider.controls.password.value
      formValue = this.signupFormProvider.value;
      formValue['usertype'] = 'provider';
      formValue.skillset = [];
      formValue.time = this.signupFormProvider.controls.fromTime.value + "-" + this.signupFormProvider.controls.toTime.value;
      const skills = this.signupFormProvider.controls.selectedSkills.value;
      skills.forEach(element => {
        const obj = {
          name: element,
          price: this.signupFormProvider.controls.price.value
        };
        formValue.skillset.push(obj);
      });
      formValue.days = this.signupFormProvider.controls.selectedDays.value;
      delete formValue['selectedSkills'];
      delete formValue['selectedDays'];
      delete formValue['fromTime'];
      delete formValue['toTime'];
      delete formValue['password'];
      delete formValue['price'];
    }
    console.log(formValue);
    this.loginService.registerUser(formValue, password).subscribe(response => {
      if (response.success) {
        this.openSnackBar(response.data.message, 'mat-primary');
        this.router.navigate(['/login']);

      }
    },  error => {
      this.openSnackBar(error.error.message, 'mat-warn');
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
  handleFileInput(files: FileList) {
    this.signupFormProvider.controls.image.setValue(files.item(0));
  }

}

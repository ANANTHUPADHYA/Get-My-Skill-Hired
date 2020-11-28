import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { servicesList, days, timings } from 'src/app/core/config';
import { ProfileService, UserParams } from 'src/app/core/services';

@Component({
  selector: 'app-provider-profile',
  templateUrl: './provider-profile.component.html',
  styleUrls: ['./provider-profile.component.scss']
})
export class ProviderProfileComponent implements OnInit {
  public signupFormProvider: FormGroup;
  public skillset = servicesList;
  public days = days;
  public timing = timings;
  public selectedDays = [];
  public toTimeArray = [];
  public selectedSkills = [];
  public showAddSkill = true;
  public userProfile;
  public isDisabled = true;
  constructor(private formBuilder: FormBuilder, private profileService: ProfileService, private snackBar: MatSnackBar) { }

  ngOnInit(): void {
    this.userProfile = JSON.parse(sessionStorage.getItem('profile'));
    this.initializeForm();
  }

  edit() {
    this.signupFormProvider.enable();
    this.signupFormProvider.controls.email.disable()
  }


  initializeForm() {
    const timeArray = this.userProfile.time.split('-');
    this.signupFormProvider = this.formBuilder.group({
      email: [this.userProfile.email, Validators.email],
      firstName: [this.userProfile.firstName, Validators.required],
      lastName: [this.userProfile.lastName, Validators.required],
      address: [this.userProfile.address, Validators.required],
      area: [this.userProfile.area, Validators.required],
      city: [this.userProfile.city, Validators.required],
      phone: [this.userProfile.phone, Validators.required],
      fromTime: [timeArray[0], Validators.required],
      toTime: [timeArray[1], Validators.required],
      selectedDays: [this.userProfile.days, Validators.required],
      image: []
    });
    this.selectedSkills = this.userProfile.skillSet;
    this.signupFormProvider.disable();
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

  profileDetailsSet() {
    this.userProfile.email = this.signupFormProvider.controls.email.value;
    this.userProfile.firstName = this.signupFormProvider.controls.firstName.value;
    this.userProfile.lastName = this.signupFormProvider.controls.lastName.value;
    this.userProfile.address = this.signupFormProvider.controls.address.value;
    this.userProfile.area = this.signupFormProvider.controls.area.value;
    this.userProfile.city = this.signupFormProvider.controls.city.value;
    this.userProfile.phone = "+91"  + this.signupFormProvider.controls.phone.value.toString();
    this.userProfile.skillSet = this.selectedSkills;
    this.userProfile.time = this.signupFormProvider.controls.fromTime.value + "-" + this.signupFormProvider.controls.toTime.value;
    this.userProfile.days = this.signupFormProvider.controls.selectedDays.value;
    sessionStorage.setItem('profile', JSON.stringify(this.userProfile));
  }

  register() {
    let formValue:UserParams;
      formValue = this.signupFormProvider.value;
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
}

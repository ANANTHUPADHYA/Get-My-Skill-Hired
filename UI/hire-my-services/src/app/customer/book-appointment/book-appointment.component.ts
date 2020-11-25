import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { timings } from 'src/app/core/config';
import { BookAppointmentReq, ProviderListService } from 'src/app/core/services';

@Component({
  selector: 'app-book-appointment',
  templateUrl: './book-appointment.component.html',
  styleUrls: ['./book-appointment.component.scss']
})
export class BookAppointmentComponent implements OnInit {
  public appointmentForm: FormGroup;
  public customerDetails;
  public toTimeArray = [];
  public fromTimeArray = [];
  public timing = timings;
  constructor(@Inject(MAT_DIALOG_DATA) public data, private formBuilder: FormBuilder, private providerListService: ProviderListService) { 
    this.appointmentForm = this.formBuilder.group({
      date: ['', Validators.required],
      fromTime: ['', Validators.required],
      toTime: ['', Validators.required],      
    });
  }

  ngOnInit(): void {
    this.customerDetails = JSON.parse(sessionStorage.getItem('profile'));
    this.populateFromTiming();
  }

  populateFromTiming() {
    const fromTime = this.data.provider.time.split('-');
    const selectedIndex= this.timing.indexOf(fromTime[0]);
   this.fromTimeArray = this.timing.slice(selectedIndex);
  }

  populateToTiming() {
    let time: number;
    this.toTimeArray = [];
    this.appointmentForm.setControl('toTime', new FormControl('', Validators.required));
    const selectedIndex= this.timing.indexOf(this.appointmentForm.controls.fromTime.value);
    this.toTimeArray = this.timing.slice(selectedIndex+1);
  }

  scheduleAppointment() {
    let params = {
      customerEmail:this.customerDetails.email,
    providerEmail: this.data.provider.email,
   serviceType:this.data.serviceType,
   date: this.appointmentForm.controls.date.value,
   time: this.appointmentForm.controls.fromTime.value + "-" + this.appointmentForm.controls.toTime.value
    }
    console.log(params);
    this.providerListService.scheduleAppointment(params).subscribe(response => {

    })
  }



}

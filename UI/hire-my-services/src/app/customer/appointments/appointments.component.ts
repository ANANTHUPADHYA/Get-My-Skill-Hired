import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-appointments',
  templateUrl: './appointments.component.html',
  styleUrls: ['./appointments.component.scss']
})
export class AppointmentsComponent implements OnInit {
public appointments = [];
  constructor() { }

  ngOnInit(): void {
  }

  getColor(status: string) {
    if(status === 'completed') {
      return 'primary';
    } else if(status === 'upcoming') {
      return 'accent';
    }  else if(status === 'cancelled') {
      return 'warn';
    }  
  }

  getListOfAppointments() {
    
  }

}

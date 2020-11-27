import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Appointment, AppointmentList, ChangeStatusParams, ProviderListService } from 'src/app/core/services';
import { ReviewComponent } from '../review/review.component';

@Component({
  selector: 'app-appointments',
  templateUrl: './appointments.component.html',
  styleUrls: ['./appointments.component.scss']
})
export class AppointmentsComponent implements OnInit {
public appointments:Appointment[] = [];
public uuid: string;
public searchKey: string;
private originalList = [];
public statusFilter = [];


  constructor(private providerListService: ProviderListService, private snackBar: MatSnackBar, private dialog: MatDialog) { }

  ngOnInit(): void {
    this.uuid = JSON.parse(sessionStorage.getItem('profile')).uuid;
    this.getListOfAppointments();
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
    this.providerListService.getListOfAppointments(this.uuid).subscribe(response => {
      if(response.success === 'true'){
        this.appointments = response.data;
        this.originalList = response.data.slice();
      }    
    }, error => {
      this.openSnackBar(error.error.data, 'mat-warn')
    });
  }

  openSnackBar(message: string, className: string) {
    this.snackBar.open(message, '', {
      duration: 5000,
      panelClass: ['mat-toolbar', className]
    });
  }


  search() {
    if (this.searchKey && this.searchKey !== '') {
      const listOfData:Appointment[] = this.originalList.slice();
      this.appointments = listOfData.filter((app) => {
        return (app.appointmentID.toLowerCase().includes(this.searchKey.toLowerCase()))
      });
    } else {
      this.appointments = this.originalList.slice();                 
    }
  }

  keyupFilter() {
    if (this.searchKey === '') {
      this.search();
    }
  }
  applyFilters() {
    let filteredAppointments:Appointment[] = this.originalList.slice();
    if (this.statusFilter.length) {
      filteredAppointments = filteredAppointments.filter(
        appt => this.statusFilter.includes(appt.status)
      );
    }
    
    this.appointments = filteredAppointments.slice();
  }

  clearFilters() {
    this.appointments = this.originalList.slice();
    this.statusFilter = [];

}

goToReview(appointment:Appointment) {
  this.dialog.open(ReviewComponent, {
    data: {
      appointment: appointment,
    },
    height: '400px',
    width: '600px'
  });
}

cancelAppointment(appId: string) {
  const params: ChangeStatusParams = {
    uuid: this.uuid,
    appId: appId,
    status: 'cancelled'
  }
  this.providerListService.changeApptStatus(params).subscribe(response => {
    if(response.success === 'true') {
      this.openSnackBar(response.Message, 'mat-primary')
      this.getListOfAppointments();
    } 
  }, error=> {
    this.openSnackBar(error, 'mat-warn');
  })
}

}

import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ServicesComponent } from './services/services.component';
import { RouterModule } from '@angular/router';
import { CustomerRoutes } from './customer.routes';
import { MaterialModule } from '../material/material.module';
import { ProviderListComponent } from './provider-list/provider-list.component';
import { AppointmentsComponent } from './appointments/appointments.component';
import { BookAppointmentComponent } from './book-appointment/book-appointment.component';



@NgModule({
  declarations: [ServicesComponent, ProviderListComponent, AppointmentsComponent, BookAppointmentComponent],
  imports: [
    CommonModule,
    RouterModule.forChild(CustomerRoutes),
    MaterialModule
  ],
  entryComponents: [
    BookAppointmentComponent
  ]
})
export class CustomerModule { }

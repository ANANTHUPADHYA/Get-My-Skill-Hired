import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ServicesComponent } from './services/services.component';
import { RouterModule } from '@angular/router';
import { CustomerRoutes } from './customer.routes';
import { MaterialModule } from '../material/material.module';
import { ProviderListComponent } from './provider-list/provider-list.component';
import { AppointmentsComponent } from './appointments/appointments.component';
import { BookAppointmentComponent } from './book-appointment/book-appointment.component';
import { ReviewComponent } from './review/review.component';
import { CustomerProfileComponent } from './customer-profile/customer-profile.component';



@NgModule({
  declarations: [ServicesComponent, ProviderListComponent, AppointmentsComponent, BookAppointmentComponent, ReviewComponent, CustomerProfileComponent],
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

import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProviderAppointmentsComponent } from './provider-appointments/provider-appointments.component';
import { ProviderProfileComponent } from './provider-profile/provider-profile.component';



@NgModule({
  declarations: [ProviderAppointmentsComponent, ProviderProfileComponent],
  imports: [
    CommonModule
  ]
})
export class ProviderModule { }

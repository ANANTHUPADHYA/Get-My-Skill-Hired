import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProviderAppointmentsComponent } from './provider-appointments/provider-appointments.component';
import { ProviderProfileComponent } from './provider-profile/provider-profile.component';
import { MaterialModule } from '../material/material.module';



@NgModule({
  declarations: [ProviderAppointmentsComponent, ProviderProfileComponent],
  imports: [
    CommonModule,
    MaterialModule
  ]
})
export class ProviderModule { }

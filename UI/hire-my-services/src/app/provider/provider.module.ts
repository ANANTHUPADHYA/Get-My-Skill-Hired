import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProviderAppointmentsComponent } from './provider-appointments/provider-appointments.component';
import { ProviderProfileComponent } from './provider-profile/provider-profile.component';
import { MaterialModule } from '../material/material.module';
import { RouterModule } from '@angular/router';
import { ProviderRoutes } from './provider.routes';



@NgModule({
  declarations: [ProviderAppointmentsComponent, ProviderProfileComponent],
  imports: [
    CommonModule,
    MaterialModule,
    RouterModule.forChild(ProviderRoutes),
  ]
})
export class ProviderModule { }

import { Routes } from '@angular/router';
import { ProviderAppointmentsComponent } from './provider-appointments/provider-appointments.component';
import { ProviderProfileComponent } from './provider-profile/provider-profile.component';

export const ProviderRoutes: Routes = [
  {path: '', component: ProviderAppointmentsComponent},
  {path: 'profile', component: ProviderProfileComponent}
];

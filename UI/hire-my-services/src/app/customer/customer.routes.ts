import { Routes } from '@angular/router';
import { ServicesComponent } from './services/services.component';
import { ProviderListComponent } from './provider-list/provider-list.component';
import { AppointmentsComponent } from './appointments/appointments.component';
import { CustomerProfileComponent } from './customer-profile/customer-profile.component';

export const CustomerRoutes: Routes = [
  {path: '', component: ServicesComponent},
  {path: 'appointments', component: AppointmentsComponent},
  {path:'provider/:service', component:ProviderListComponent},
  {path: 'profile', component: CustomerProfileComponent}
];

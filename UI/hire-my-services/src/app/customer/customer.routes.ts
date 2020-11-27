import { Routes } from '@angular/router';
import { ServicesComponent } from './services/services.component';
import { ProviderListComponent } from './provider-list/provider-list.component';
import { AppointmentsComponent } from './appointments/appointments.component';

export const CustomerRoutes: Routes = [
  {path: '', component: ServicesComponent},
  {path: 'appointments', component: AppointmentsComponent},
  {path:'provider/:service', component:ProviderListComponent}
];

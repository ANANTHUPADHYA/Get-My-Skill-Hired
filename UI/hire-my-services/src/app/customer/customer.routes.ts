import { Routes } from '@angular/router';
import { ServicesComponent } from './services/services.component';
import { ProviderListComponent } from './provider-list/provider-list.component';

export const CustomerRoutes: Routes = [
  {path: '', component: ServicesComponent},
  {path:'provider/:service', component:ProviderListComponent}
];

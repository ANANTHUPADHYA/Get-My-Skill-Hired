import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ServicesComponent } from './services/services.component';
import { RouterModule } from '@angular/router';
import { CustomerRoutes } from './customer.routes';
import { MaterialModule } from '../material/material.module';
import { ProviderListComponent } from './provider-list/provider-list.component';



@NgModule({
  declarations: [ServicesComponent, ProviderListComponent],
  imports: [
    CommonModule,
    RouterModule.forChild(CustomerRoutes),
    MaterialModule
  ]
})
export class CustomerModule { }

import { Component, OnInit } from '@angular/core';
import { ProviderListService, ProviderDetails } from 'src/app/core/services';
import { MatSnackBar } from '@angular/material/snack-bar';
import { servicesList } from 'src/app/core/config';
import { Subscription } from 'rxjs';
import { ActivatedRoute } from '@angular/router';
import {MatDialog, MAT_DIALOG_DATA} from '@angular/material/dialog';
import { BookAppointmentComponent } from '../book-appointment/book-appointment.component';

@Component({
  selector: 'app-provider-list',
  templateUrl: './provider-list.component.html',
  styleUrls: ['./provider-list.component.scss']
})
export class ProviderListComponent implements OnInit {

  public searchKey: string;
  public priceFilter: number;
  public ratingFilter: number;
  public services = servicesList;
  public listOfProviders: ProviderDetails[];
  private originalList: ProviderDetails[];
  private subscriptions = new Subscription();
  public serviceType: string;
  constructor(
    private providerListService: ProviderListService,
    private snackBar: MatSnackBar,
    private activatedRoute: ActivatedRoute,
    public dialog: MatDialog
  ) {}
  ngOnInit() {
    this.listOfProviders = [];
    this.originalList = [];
    this.services = [];
    this.activatedRoute.params.subscribe(data => {
      this.serviceType = data.service;
    });
    this.getlistOfProviders();
  }
  openSnackBar(message: string, className: string) {
    this.snackBar.open(message, '', {
      duration: 5000,
      panelClass: ['mat-toolbar', className]
    });
  }


  getlistOfProviders() {
    this.subscriptions.add(
      this.providerListService.getListOfProviders(this.serviceType).subscribe(
        response => {
          if (response.success === 'true') {
            this.listOfProviders = response.data;
            this.originalList = response.data.slice();
          }
        },
        error => {
          this.openSnackBar(error.error.error, 'mat-warn');
        }
      )
    );
  }
  searchProviders() {
    if (this.searchKey && this.searchKey !== '') {
      const listOfData = this.originalList.slice();
      this.listOfProviders = listOfData.filter((product) => {
        return (product.area.toLowerCase().includes(this.searchKey.toLowerCase()) || product.city.toLowerCase().includes(this.searchKey.toLowerCase()) )
      });
    } else {
      this.listOfProviders = this.originalList.slice();                
    }
  }

  keyupFilter() {
    if (this.searchKey === '') {
      this.searchProviders();
    }
  }
  applyFilters() {
    let filteredProviders = this.originalList.slice();

    if (this.priceFilter) {
      filteredProviders = filteredProviders.filter(
        provider => parseInt(provider.price) <= +this.priceFilter
      );
    }
    if (this.ratingFilter) {
      filteredProviders = filteredProviders.filter(
        provider => provider.rating === this.ratingFilter
      );
    }
    this.listOfProviders = filteredProviders.slice();
  }

  clearFilters() {
    this.listOfProviders = this.originalList.slice();
    this.priceFilter = 100;
    this.ratingFilter = 1;

  }
  formatLabel(value: number): number | string {
    if (value >= 1000) {
      return Math.round(value / 1000) + 'k';
    }

    return value;
  }


  ngOnDestroy() {
    this.subscriptions.unsubscribe();
  }

numberOfFullStars(rating): number {
    return rating;
  }

    numberOfEmptyStars(rating): number {
    return 5 - rating;
  }

 fullStars(rating:string): any[] {
    
    return Array(this.numberOfFullStars(parseInt(rating)));
  }

 emptyStars(rating): any[] {
    return Array(this.numberOfEmptyStars(parseInt(rating)));
  }

  openAppointmentBookingComp(providerDetails: any) {
    this.dialog.open(BookAppointmentComponent, {
      data: {
        provider: providerDetails,
        serviceType: this.serviceType,
      },
      height: '700px',
      width: '550px'
    });
  }

}

import { Component, OnInit } from '@angular/core';
import { servicesList } from 'src/app/core/config';
import { Router } from '@angular/router';

@Component({
  selector: 'app-services',
  templateUrl: './services.component.html',
  styleUrls: ['./services.component.scss']
})
export class ServicesComponent implements OnInit {
public services = servicesList;
  constructor(private router: Router) { }

  ngOnInit(): void {
    const sessionID = sessionStorage.getItem('sessionID');
    if(!sessionID) {
      this.router.navigate(['login']);
    }
  }


  goToProviderList(service: string) {
    this.router.navigate(['customer/provider', service])
  }


}

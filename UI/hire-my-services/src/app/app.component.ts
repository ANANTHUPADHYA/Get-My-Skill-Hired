import { Component, OnInit } from '@angular/core';
import { SharedService } from './core/services';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit{
  title = 'hire-my-services';
  showSpinner = false;

  constructor(private sharedService: SharedService) {}

  ngOnInit() {
    this.sharedService.showSppiner.subscribe(data => {
      this.showSpinner = data;
    })
  }
}

import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SharedService {
  public userLoggedIn = new Subject<boolean>();
  public showSppiner = new Subject<boolean>();
  constructor() { }
}

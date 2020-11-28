import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ProviderListService, ReviewParams } from 'src/app/core/services';

@Component({
  selector: 'app-review',
  templateUrl: './review.component.html',
  styleUrls: ['./review.component.scss']
})
export class ReviewComponent implements OnInit {
public reviewForm: FormGroup;
  constructor(private formBuilder: FormBuilder, @Inject(MAT_DIALOG_DATA) public data, private providerListService: ProviderListService, private snackBar: MatSnackBar) { 
    this.reviewForm = this.formBuilder.group({
      review: ['', Validators.email],
      rating: [1, Validators.required],
  });
}

openSnackBar(message: string, className: string) {
  this.snackBar.open(message, '', {
    duration: 5000,
    panelClass: ['mat-toolbar', className]
  });
}

reviewSubmit() {

  const params: ReviewParams = this.reviewForm.value;
  params.rating = params.rating.toString();
  params.appId = this.data.appointmentID;
  params.uuid = JSON.parse(sessionStorage.getItem('profile')).uuid;

  this.providerListService.postReview(params).subscribe(response => {
    if(response.success) {
      this.openSnackBar(response.Message, 'mat-primary')
    }
  });


}


  ngOnInit(): void {
  }

}

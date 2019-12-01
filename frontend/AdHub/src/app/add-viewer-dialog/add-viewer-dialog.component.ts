import { Component, OnInit } from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {MatDialogRef} from '@angular/material';

@Component({
  selector: 'app-add-viewer-dialog',
  templateUrl: './add-viewer-dialog.component.html',
  styleUrls: ['./add-viewer-dialog.component.css']
})
export class AddViewerDialogComponent implements OnInit {

  private readonly types = ['Food','Car','Furniture','Fitness'];
  private includedTypeController = new FormControl('');


  constructor(public dialogRef: MatDialogRef<AddViewerDialogComponent>) { }

  ngOnInit() {

  }

  closeDialog(save: boolean){

    console.log(this.includedTypeController.value);

    if(save){
      this.dialogRef.close({
        included_types: this.includedTypeController.value
      });
    }else{
      this.dialogRef.close(null);
    }

  }

}

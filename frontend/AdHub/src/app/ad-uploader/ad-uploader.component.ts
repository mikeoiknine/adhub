import {Component, Inject, OnInit} from '@angular/core';
import {FileService} from '../services/file.service';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {connectableObservableDescriptor} from 'rxjs/internal/observable/ConnectableObservable';

@Component({
  selector: 'app-ad-uploader',
  templateUrl: './ad-uploader.component.html',
  styleUrls: ['./ad-uploader.component.css']
})
export class AdUploaderComponent implements OnInit {

  private types = ['Food','Car','Furniture','Fitness'];
  private base64File = null;
  private file :File = null;
  private uploadForm = new FormGroup({
      nameController: new FormControl('', [Validators.required]),
      typeController: new FormControl('', [Validators.required])
    }
  )

  constructor(private fileService: FileService, public dialogRef: MatDialogRef<AdUploaderComponent>) { }

  ngOnInit() {
  }

  uploadFile(event) {
    this.file = event[0];
      const reader = new FileReader();


      reader.onload = (e) => {
        const binaryString = reader.result;
        const base64textString = btoa(binaryString.toString());
        this.base64File = 'data:'+ this.file.type + ';base64,' + base64textString;
        console.log(this.base64File);
      } ;

      this.base64File = reader.readAsBinaryString(this.file);
      console.log(this.base64File);

  }

  closeDialog(save: boolean){
    if(save){
      this.dialogRef.close({
        name: this.uploadForm.controls['nameController'].value,
        base64: this.base64File,
        type: this.uploadForm.controls['typeController'].value
      });
    }else{
      this.dialogRef.close(null);
    }

  }

  deleteAttachment() {
    this.file = null;
  }

}

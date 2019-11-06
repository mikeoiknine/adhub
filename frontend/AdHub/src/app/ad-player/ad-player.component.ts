import {Component, Input, OnInit} from '@angular/core';
import {MatSnackBar} from '@angular/material';

@Component({
  selector: 'app-ad-player',
  templateUrl: './ad-player.component.html',
  styleUrls: ['./ad-player.component.css']
})
export class AdPlayerComponent implements OnInit {


  @Input()
  image_base_64: String;

  constructor(private _snackBar: MatSnackBar) { }

  ngOnInit() {
    this._snackBar.open('Press ESC to stop playing add', '', {
      duration: 2000,
      horizontalPosition: 'center',
      verticalPosition:'top',
      panelClass :'center'
    });
  }



}

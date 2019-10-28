import { Component, OnInit } from '@angular/core';
import {AdItem, AdItemStats, User} from '../models/models';
import {AdvertisementService} from '../services/advertisement.service';
import {AuthService} from '../services/auth.service';
import {MatDialog} from '@angular/material';
import {AdUploaderComponent} from '../ad-uploader/ad-uploader.component';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  private ads: AdItem[];
  private user: User;

  constructor(private adService: AdvertisementService, private authService: AuthService, private dialog: MatDialog) { }

  ngOnInit() {
    this.ads = this.adService.getAdvertisement();
    this. user = this.authService.getMe();
  }

  openAdUploadDialog(){
    const dialogRef = this.dialog.open(AdUploaderComponent, {
      width: '45%',
    });

    dialogRef.afterClosed().subscribe(result => {

      if(result) {
        this.ads.push({
          id: '1',
          stats: {
            numberOfTimeSeeMonth: 0,
            numberOfTimeSeeWeek: 0,
            numberOfTimeSeeDay: 0
          },
          uploadedDate: new Date(),
          name: result['name'],
          userId: this.user.id,
          imagePath: 'some path',
          image_64: result['base64']
        });
      }
    });
  }
}

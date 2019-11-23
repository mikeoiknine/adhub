import {Component, HostListener, OnInit} from '@angular/core';
import {AdItem, AdItemStats, User} from '../models/models';
import {AdvertisementService} from '../services/advertisement.service';
import {AuthService} from '../services/auth.service';
import {MatDialog} from '@angular/material';
import {AdUploaderComponent} from '../ad-uploader/ad-uploader.component';
import {image_base_64} from '../mockData/mockAds';
import {animate, style, transition, trigger} from '@angular/animations';
import {AddViewerDialogComponent} from '../add-viewer-dialog/add-viewer-dialog.component';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css'],
  animations: [
    trigger('fadeInOut', [
      transition(':enter', [   // :enter is alias to 'void => *'
        style({opacity: 0}),
        animate(300, style({opacity: 1}))
      ]),
      transition(':leave', [   // :leave is alias to '* => void'
        animate(300, style({opacity: 0}))
      ])
    ])
  ]
})
export class DashboardComponent implements OnInit {

  private ads: AdItem[];
  private user: User;
  private viewerEnable = false;
  private viewingImage: String = null;

  constructor(private adService: AdvertisementService, private authService: AuthService, private dialog: MatDialog) {
  }

  ngOnInit() {
    this.ads = this.adService.getAdvertisement();
    this.user = this.authService.getMe();
  }

  openAdUploadDialog() {
    const dialogRef = this.dialog.open(AdUploaderComponent, {
      width: '45%',
    });

    dialogRef.afterClosed().subscribe(result => {

      if (result) {
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

  openImageViewer() {

    const dialogRef = this.dialog.open(AddViewerDialogComponent, {
      width: '45%',
    });

    dialogRef.afterClosed().subscribe(result => {

      if (result) {
        this.viewerEnable = true;
        this.viewingImage = image_base_64;
      }
    });

  }

  async delay(ms: number) {
    await new Promise(resolve => setTimeout(() => resolve(), ms)).then(() => console.log('fired'));
  }

  @HostListener('document:keydown.escape', ['$event']) onKeydownHandler(event: KeyboardEvent) {
    console.log('Escape pressed');
    this.delay(300).then(any => {
      this.viewerEnable = false;
      this.viewingImage = null;
    });
  }
}

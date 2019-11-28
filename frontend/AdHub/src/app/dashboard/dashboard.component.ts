import {Component, HostListener, OnInit} from '@angular/core';
import {AdItem, AdItemStats, User} from '../models/models';
import {AdvertisementService} from '../services/advertisement.service';
import {AuthService} from '../services/auth.service';
import {MatDialog, MatSnackBar} from '@angular/material';
import {AdUploaderComponent} from '../ad-uploader/ad-uploader.component';
import {image_base_64} from '../mockData/mockAds';
import {animate, style, transition, trigger} from '@angular/animations';
import {AddViewerDialogComponent} from '../add-viewer-dialog/add-viewer-dialog.component';
import {Subscription} from 'rxjs';

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

  private allAds: AdItem[] = [];
  private user: User;
  private viewerEnable = false;
  private viewingImage: string = null;
  private viewingImageID: string = null;

  private expenses = 0;
  private revenue = 0;


  private activeSubscription: Subscription = null;

  constructor(private adService: AdvertisementService, private authService: AuthService, private dialog: MatDialog, private snackBar: MatSnackBar) {
  }

  ngOnInit() {
    this.adService.getMyAds().subscribe((result) => {
      const ads = (result['ads'] as Array<any>).map((item) => {
        item['upload_date'] = new Date(item['upload_date']);
        return item;
      });
      this.allAds = ads;
    }, () => {
      this.snackBar.open('Cannot connect to server. Try again', '', {
        duration: 2000
      });
    });

    this.authService.getMe().subscribe((result) => {
        this.user = result;
      },
      (error) => {
        this.snackBar.open('Cannot connect to server. Try again', '', {
          duration: 2000
        });
      });

    this.adService.getExpenses().subscribe((result) => {
        this.expenses = result['expense'];
      },
      (error) => {
        this.snackBar.open('Cannot connect to server. Try again', '', {
          duration: 2000
        });
      });

    this.adService.getRevenue().subscribe((result) => {
        this.revenue = result['revenue'];
      },
      (error) => {
        this.snackBar.open('Cannot connect to server. Try again', '', {
          duration: 2000
        });
      });
  }

  openAdUploadDialog() {
    const dialogRef = this.dialog.open(AdUploaderComponent, {
      width: '45%',
    });

    dialogRef.afterClosed().subscribe(result => {

      if (result) {

        this.adService.uploadAd(result['name'], result['type'], result['location'], result['base64'])
          .subscribe((ad) => {

            this.allAds.push({
              _id: ad['ad_id'],
              stats: {
                total_view_count: 0,
                year_view_count: 0,
                month_view_count: 0,
                day_view_count: 0
              } as AdItemStats,
              region: result['location'],
              uploaded_date: new Date(),
              is_active: true,
              category: result['type'],
              name: result['name'],
              user_id: this.user.id,
              image_path: 'some path',
              image_64: result['base64']
            });
          }, (error) => {
            console.log('Error when uploading image' + error.error.message);
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
        this.startStreamingAds(result['included_types']);
      }
    });

  }

  changeActiveState(item: AdItem, state: boolean) {
    const ad_id = this.allAds.find((ad) => ad === item)._id;
    this.adService.setActiveStatus(ad_id, state).subscribe(() => {
        this.allAds.find((ad) => ad === item).is_active = state;
      }, (error) => {
      this.snackBar.open('Could not change active status of ad with id: ' + ad_id + ' Error: ' + error.error.message, '', {
        duration: 1000,
      });
    });

  }

  deleteAd(id: string) {

    const adToDelete = this.allAds.find((ad) => ad._id === id);

    this.adService.deleteAd(id).subscribe(() => {
      this.snackBar.open('Ad deleted: ' + adToDelete.name, '', {
        duration: 1000,
      });

      this.allAds.splice(this.allAds.indexOf(adToDelete), 1);

    }, (error) => {
      this.snackBar.open('Could not delete ad with id: ' + id + ' Error: ' + error.error.message, '', {
        duration: 1000,
      });
    });
  }

  logout() {
    this.authService.logout();
  }

  async delay(ms: number) {
    await new Promise(resolve => setTimeout(() => resolve(), ms)).then(() => console.log('fired'));
  }

  async startStreamingAds(included: string[]) {
    await this.adService.sendConfiguration(included).subscribe(() => {

     this.getNextAd();

      this.activeSubscription = this.adService.startStreaming().subscribe(() => {
        this.getNextAd();
      });
    }, () => {
      this.snackBar.open('Cannot connect to server. Try again', '', {
      duration: 2000
    }); });
  }

  getNextAd(){
    // Get first ad
    this.adService.getNextAdd(this.viewingImageID).subscribe((obj) => {
      this.viewerEnable = true;
      this.viewingImageID = obj['ad_id'];
      this.viewingImage = obj['image_64'];
      console.log('Got image: ' + this.viewingImageID);

    }, (error) => {
      if(error.status === 510){
        this.snackBar.open('No image matches the your location and category', '', {
          duration: 2000
        });
      }else {
        console.log('Cannot connect to server');
      }
      this.closeAdStreaming();
    });
  }

  closeAdStreaming() {
    this.viewerEnable = false;
    this.viewingImage = null;
    this.activeSubscription.unsubscribe();
  }

  @HostListener('document:keydown.escape', ['$event']) onKeydownHandler(event: KeyboardEvent) {
    console.log('Escape pressed');
    this.delay(300).then(any => {
      this.closeAdStreaming();
    });
  }
}

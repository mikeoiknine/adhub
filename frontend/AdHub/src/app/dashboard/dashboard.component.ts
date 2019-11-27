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

  private activeSubscription: Subscription = null;

  constructor(private adService: AdvertisementService, private authService: AuthService, private dialog: MatDialog, private snackBar: MatSnackBar) {
  }

  ngOnInit() {
    this.adService.getMyAds().subscribe((result) => {
      this.allAds = Array.from( result['ads'].values());
    }, ()=> {
      this.snackBar.open('Cannot connect to server. Try again', '', {
        duration: 2000
      });
    });
    this.authService.getMe().subscribe((result) =>{
        this.user = result;
      },
      (error) => {
        console.log('Error when fetching active user');
    });
  }

  openAdUploadDialog() {
    const dialogRef = this.dialog.open(AdUploaderComponent, {
      width: '45%',
    });

    dialogRef.afterClosed().subscribe(result => {

      if (result) {
        this.allAds.push({
          id: '1',
          stats: {
            numberOfTimeSeeMonth: 0,
            numberOfTimeSeeWeek: 0,
            numberOfTimeSeeDay: 0
          },
          uploadedDate: new Date(),
          active: true,
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

  changeActiveState(item: AdItem, state: boolean) {

    this.allAds.find((ad) => ad === item).active = state;
  }

  deleteAd(id: string){

  const adToDelete = this.allAds.find((ad) => ad.id === id);

    this.adService.deleteAd(id).subscribe(() => {
      this.snackBar.open('Ad deleted: ' +adToDelete.name , '',{
        duration: 1000,
      } );

      this.allAds.splice(this.allAds.indexOf(adToDelete), 1);

    }, (error) => {
      this.snackBar.open('Could not delete ad with id: '+  id + ' Error: '+ error.error.message, '',{
        duration: 1000,
      } );
    });
  }

  logout(){
    this.authService.logout();
  }

  async delay(ms: number) {
    await new Promise(resolve => setTimeout(() => resolve(), ms)).then(() => console.log('fired'));
  }

  async startStreamingAds(included: string[]){
    await this.adService.sendConfiguration(included);

    this.activeSubscription = this.adService.startStreaming().subscribe(() => {
      this.adService.getNextAdd(this.viewingImageID).subscribe( (obj) => {
        this.viewingImageID = obj['ad_id'];
        this.viewingImageID = obj['image_64'];
      }, (error) => {
        this.closeAdStreaming();
      });
    });
  }

  closeAdStreaming(){
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

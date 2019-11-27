import { Injectable } from '@angular/core';
import mockAds from '../mockData/mockAds';
import {AdItem} from '../models/models';
import {HttpClient, HttpParams} from '@angular/common/http';
import {host} from '../../environments/environment';
import {Observable} from 'rxjs';
import { interval } from 'rxjs';
import {AuthService} from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class AdvertisementService {
  private readonly PATH = '/data/';
  private readonly CONFIG_PATH = 'config';
  private readonly ADD_AD = 'add';
  private readonly NEXT = 'next';
  private readonly GET_MY_ADS = 'ads';
  private readonly DELETE_AD = 'DELETE';
  private readonly CHANGE_ACTIVE_AD = '';

  private periodicSubscriber: Observable<any>;

  constructor(private http: HttpClient, private authService: AuthService) { }

  getMyAdvertisement(): AdItem[]{
    return mockAds;
  }

  uploadAd(name: string, category: String, locations: string[], image_64: string){
    const body = {
      name: name,
      user_id: this.authService.getMyId(),
      region: locations,
      upload_date: Date(),
      category: category,
      image_64: image_64
    };
    return this.http.post(host + this.PATH + this.ADD_AD, body);
  }

  deleteAd(id: string){
    const params = new HttpParams()
      .set('ad_id', id)
      .set('user_id', this.authService.getMyId());
    return this.http.delete(host + this.PATH + this.DELETE_AD, {params: params});
  }

  sendConfiguration(included: string[]){
    return this.http.post(host + this.PATH + this.CONFIG_PATH, included);
  }

  startStreaming(): Observable<any>{
     this.periodicSubscriber = interval(30000);

     return this.periodicSubscriber;
  }

  getNextAdd(lastAdSeen: string){
    const params = new HttpParams()
      .set('last_ad_id', lastAdSeen)
      .set('user_id', this.authService.getMyId());

    return this.http.get(host + this.PATH + this.NEXT, {params: params});
  }

  getMyAds(){
    const params = new HttpParams()
      .set('user_id', this.authService.getMyId());

    return this.http.get(host + this.PATH + this.GET_MY_ADS, {params: params});
  }

}

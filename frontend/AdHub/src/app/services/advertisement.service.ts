import { Injectable } from '@angular/core';
import mockAds from '../mockData/mockAds';
import {AdItem} from '../models/models';
import {HttpClient, HttpParams} from '@angular/common/http';
import {host} from '../../environments/environment';
import {Observable} from 'rxjs';
import {AuthService} from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class AdvertisementService {
  private readonly VIEW_ADS_PATH = '/data/';

  constructor(private http: HttpClient, private authService: AuthService) { }

  getMyAdvertisement(): AdItem[]{
    return mockAds;
  }

  uploadAd(name: string, category: String, locations: string[], image_64: string){
    const body = {
      name: name,
      category: category,
      locations: locations,
      image_64: image_64
    };
    return this.http.post(host + this.VIEW_ADS_PATH, body);
  }

  getNextAdvertisement(excluded: string[], numberToBuffer: Number): Observable<AdItem[]>{

    const params =  new HttpParams()
    .append('excluded', excluded.join(','))
    .set('numberToBuffer', numberToBuffer.toString());

   return this.http.get<any>(host + this.VIEW_ADS_PATH, {params: params});
  }

  deleteAd(id: string){
    const params = new HttpParams().set('imageId', id);
    return this.http.delete(host + this.VIEW_ADS_PATH, {params: params});
  }

  sendConfirmation(imageId: string){
    this.http.put(host + this.VIEW_ADS_PATH, {imageId: imageId}).subscribe(()=>{},()=>{
      console.log('Error when sending confirmation for: ' + imageId);
    });
  }
}

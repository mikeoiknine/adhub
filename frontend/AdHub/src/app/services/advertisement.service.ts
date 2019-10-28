import { Injectable } from '@angular/core';
import mockAds from '../mockData/mockAds';
import {AdItem} from '../models/models';

@Injectable({
  providedIn: 'root'
})
export class AdvertisementService {

  constructor() { }

  getAdvertisement(): AdItem[]{
    return mockAds;
  }
}

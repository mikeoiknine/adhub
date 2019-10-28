import { Injectable } from '@angular/core';
import mockUser from '../mockData/mockUser';
import {User} from '../models/models';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor() { }

   isUserAuthenticated() {
    return true;
   }

  login(value: any, value2: any) {
    return true;
  }

  getMe(): User {
    return mockUser;
  }
}

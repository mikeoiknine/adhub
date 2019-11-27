import { Injectable } from '@angular/core';
import mockUser from '../mockData/mockUser';
import {User} from '../models/models';
import {HttpClient} from '@angular/common/http';
import {Router} from '@angular/router';
import {host} from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  readonly PATH ='/auth/';
  readonly LOGIN_PATH ='login';
  readonly REGISTER_PATH ='register';


  constructor(private http: HttpClient, private router: Router) { }

   isUserAuthenticated() {
    return this.getState() != null;
   }

  login(username: String, password: String) {

    const params = {username: username, password: password};

    this.http.post(host + this.PATH + this.LOGIN_PATH, params).subscribe(value => {
      this.saveState(value['id']);
      this.router.navigate(['/dashboard']);
      console.log('yay');
    },error => {
      console.log('nope');
    });
  }

  register(name: string, email: string, password: string, location: string, businessName: string){

    const params = {
      name: name,
      email: email,
      password: password,
      location: location,
      businessName: businessName
    };

    this.http.post(host + this.PATH + this.REGISTER_PATH, params).subscribe(value => {
      this.router.navigate(['/login']);
      console.log('registered');
    },error => {
      console.log('nope');
    });
  }

  logout(){
    this.saveState(null);
    this.router.navigate(['/login']);
  }

  getMe(): User {
    return mockUser;
  }

  saveState(userId){
    if(!userId){
      localStorage.removeItem('adhub_userId');
    }else {
      localStorage.setItem('adhub_userId', userId);
    }
  }

  getState(){
    return localStorage.getItem('adhub_userId');
  }

}

import { Injectable } from '@angular/core';
import mockUser from '../mockData/mockUser';
import {User} from '../models/models';
import {HttpClient, HttpParams} from '@angular/common/http';
import {Router} from '@angular/router';
import {host} from '../../environments/environment';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  readonly AUTH_PATH ='/auth/';
  readonly DATA_PATH = '/data/';
  readonly LOGIN_PATH ='login';
  readonly REGISTER_PATH ='register';
  readonly ME_PATH ='me';


  constructor(private http: HttpClient, private router: Router) { }

   isUserAuthenticated() {
    return this.getState() != null;
   }

  login(username: String, password: String) {

    const params = {username: username, password: password};

    this.http.post(host + this.AUTH_PATH + this.LOGIN_PATH, params).subscribe(value => {
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
      username: email,
      password: password,
      location: location,
      businessName: businessName
    };

    this.http.post(host + this.AUTH_PATH + this.REGISTER_PATH, params).subscribe(value => {
      this.router.navigate(['/login']);
      console.log('registered');
    },error => {
      console.log('nope');
    });
  }

  logout(){
    localStorage.removeItem('adhub_userId');
    this.router.navigate(['/login']);
  }

  getMe(): Observable<User> {
    const params = new HttpParams().set('user_id', this.getState());
    return this.http.get<User>(host + this.DATA_PATH + this.ME_PATH, {params: params});
  }

  saveState(userId){
    localStorage.setItem('adhub_userId', userId);
  }

  getState(){
    return localStorage.getItem('adhub_userId');
  }

  getMyId(){
    return this.getState();
  }

}

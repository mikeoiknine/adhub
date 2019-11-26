import { Component } from '@angular/core';
import {AuthService} from './services/auth.service';
import {environment} from '../environments/environment';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'AdHub';

  constructor(private authService: AuthService){
    if(!environment.debug_login) {
      this.authService.saveState('mock');
    }
  }
}

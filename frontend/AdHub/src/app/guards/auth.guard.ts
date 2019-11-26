import {
  CanActivate,
  ActivatedRouteSnapshot,
  RouterStateSnapshot,
  Router
} from '@angular/router';

import { environment} from '../../environments/environment';
import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import { AuthService } from '../services/auth.service';

@Injectable()
export class AuthGuard implements CanActivate {
  constructor(private authService: AuthService, private router: Router) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): boolean | Observable<boolean> | Promise<boolean> {
    /* Check if mockUser is already logged in */
    const userLoggedIn = this.authService.isUserAuthenticated();

    /* If not, then cannot access route and will be redirected to the login page */
    if (!userLoggedIn) {
      this.router.navigate(['/login']);
    }

    if(environment.debug_login){
      return false;
    }else {
      return userLoggedIn;
    }
  }
}

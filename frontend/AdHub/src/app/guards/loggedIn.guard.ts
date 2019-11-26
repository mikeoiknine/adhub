import {
  CanActivate,
  ActivatedRouteSnapshot,
  RouterStateSnapshot,
  Router
} from '@angular/router';
import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import { AuthService } from '../services/auth.service';
import {environment} from '../../environments/environment';

@Injectable()
export class LoggedInGuard implements CanActivate {
  constructor(private authService: AuthService, private router: Router) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): boolean | Observable<boolean> | Promise<boolean> {
    /* Check if mockUser is already logged in */
    const userLoggedIn = this.authService.isUserAuthenticated();

    /* if the mockUser is already logged in, redirecting to the home page */


    /* return true, can activate the route since it is needed to log in */
    if(environment.debug_login){
      return true;
    }else {
      if (userLoggedIn) {
        this.router.navigate(['/']);
      }

      return !userLoggedIn;
    }

  }
}

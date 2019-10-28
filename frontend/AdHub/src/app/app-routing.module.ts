import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {LoginComponent} from './login/login.component';
import {LoggedInGuard} from './guards/loggedIn.guard';
import {AuthGuard} from './guards/auth.guard';
import {RegisterComponent} from './register/register.component';
import {DashboardComponent} from './dashboard/dashboard.component';

const routes: Routes = [
  // {path: 'register', component: RegisterComponent, canActivate: [LoggedInGuard]},
  // {path: 'login', component: LoginComponent, canActivate: [LoggedInGuard]},
  {path: 'dashboard', component: DashboardComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
  providers: [AuthGuard, LoggedInGuard]
})
export class AppRoutingModule { }

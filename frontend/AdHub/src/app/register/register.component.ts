import { Component, OnInit } from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {AuthService} from '../services/auth.service';
import {LOCATIONS} from '../models/models';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  private registerForm: FormGroup = new FormGroup({
    emailController: new FormControl('', [Validators.required]),
    nameController: new FormControl('', [Validators.required]),
    businessController: new FormControl('', [Validators.required]),
    passwordController: new FormControl('', [Validators.required]),
    locationController: new FormControl('', [Validators.required])
  });
  private hide_Password = true;
  readonly LOCATIONS = LOCATIONS;
  constructor(private authService: AuthService) { }

  ngOnInit() {
  }

  showPassword() {
    this.hide_Password = false;
  }

  hidePassword() {
    this.hide_Password = true;
  }

  sendRegistration() {
    this.authService.register(
      this.registerForm.get('nameController').value,
      this.registerForm.get('emailController').value,
      this.registerForm.get('passwordController').value,
      this.registerForm.get('locationController').value,
      this.registerForm.get('businessController').value
    );
  }

}


import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class FileService {

  constructor() { }

  getFile(file: File){}

  getBase64Image(file: File): String{
    return '';
  }

}

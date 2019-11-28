import { Pipe, PipeTransform } from '@angular/core';
import {AdItem} from '../models/models';

@Pipe({
  name: 'isActiveAd',
  pure: false
})
export class ActivePipe implements PipeTransform {
  transform(items: AdItem[], filter: string): any {
    if (!items) {
      return items;
    }
    // filter items array, items which match and return true will be
    // kept, false will be filtered out
    return items.filter(item => {
      if(filter === 'inactive') {
        return !item.is_active;
      }else{
        return item.is_active;
      }
    });
  }
}

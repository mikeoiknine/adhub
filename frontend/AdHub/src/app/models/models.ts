export interface AdItem {
  id: String;
  name: String;
  userId: String;
  imagePath: String;
  image_64: String;
  stats: AdItemStats;
  uploadedDate: Date;
  active: Boolean;
}

export interface AdItemStats {
  numberOfTimeSeeMonth: number;
  numberOfTimeSeeDay: number;
  numberOfTimeSeeWeek: number;
}

export interface User {
  name: String;
  id: String;
  email: String;
  company: String;
  address: String;
  adItems: AdItem[];
}

export const LOCATIONS = ['Downtown, Montreal', 'Old Montreal, Montreal', 'Plateau Mont-Royal, Montreal', 'Cotes-des-Neige, Montreal', 'West Island, Montreal', 'Verdun, Montreal', 'Westmount, Montreal', 'Outremont, Montreal', 'South West, Montreal', 'Hochelaga-Maisonneuve, Montreal'];
export const TYPES = ['Food', 'Car Dealership', 'Furniture', 'Fitness'];

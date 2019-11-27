export interface AdItem {
  id: string;
  name: string;
  userId: string;
  category: string;
  imagePath: string;
  image_64: string;
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
  name: string;
  id: string;
  email: string;
  company: string;
  address: string;
  ads: string[];
}

export const LOCATIONS = ['Downtown, Montreal', 'Old Montreal, Montreal', 'Plateau Mont-Royal, Montreal', 'Cotes-des-Neige, Montreal', 'West Island, Montreal', 'Verdun, Montreal', 'Westmount, Montreal', 'Outremont, Montreal', 'South West, Montreal', 'Hochelaga-Maisonneuve, Montreal'];
export const TYPES = ['Food', 'Car Dealership', 'Furniture', 'Fitness'];

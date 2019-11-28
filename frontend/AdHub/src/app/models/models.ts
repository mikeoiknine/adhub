export interface AdItem {
  ad_id: string;
  name: string;
  user_id: string;
  category: string;
  image_path: string;
  image_64: string;
  region: string[];
  stats: AdItemStats;
  uploaded_date: Date;
  active: Boolean;
}

export interface AdItemStats {
  total_view_count: number;
  year_view_count: number;
  month_view_count: number;
  day_view_count: number;
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

export interface AdItem {
  id: String;
  name: String;
  userId: String;
  imagePath: String;
  image_64: String;
  stats: AdItemStats;
  uploadedDate: Date;
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

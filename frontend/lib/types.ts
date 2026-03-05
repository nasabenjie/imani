export interface Supermarket {
  id: number;
  name: string;
  image_url: string;
  location: string;
}

export interface Product {
  id: number;
  name: string;
  price: string; 
  image_url: string;
  supermarket: number;
  supermarket_name: string;
  category: number;
  category_name: string;
}

export interface CartItem {
  id: number;
  name: string;
  price: number; 
  image_url: string;
  quantity: number;
}
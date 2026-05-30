export interface Section {
  sname: string;
  department: string;
}

export interface Supermarket {
  id: number;
  location: string;
  opening_time: string;
  close_time: string;
  sections: Section[];
  section_ids?: string[];
}

export interface Employee {
  enumber: number;
  name: string;
  role: string;
  salary: number;
  age: number;
  contact: string;
  supermarket: number;
  supermarket_location?: string;
  sex: string;
  supervisor: number | null;
  is_active: boolean;
  group?: string;
  group_name?: string;
}

export interface Product {
  prodid: number;
  name: string;
  brand: string;
  price: number;
  req_cold: boolean;
  section_name: string;
  section?: string;
}

export interface WareHStock {
  product: number;
  product_name: string;
  product_price: number;
  wqty: number;
}

export interface Warehouse {
  wnumber: number;
  area: number;
  supermarket: number;
  supermarket_location?: string;
  stock?: WareHStock[];
  product_ids?: number[];
}

export interface Distributor {
  email: string;
  contact: string;
  name: string;
}

export interface Client {
  nif: number;
  name: string;
  fidelity: number;
  address: string;
  contact: string;
}

export interface PurchaseItem {
  product: number;
  product_name?: string;
  quantity: number;
  price_at_purchase: number;
}

export interface Purchase {
  purchid: number;
  date: string;
  supermarket: number;
  client: number | null;
  client_name?: string;
  items?: PurchaseItem[];
  item_data?: { product: number; quantity: number }[];
  calculated_total?: number;
}

export interface OrderItem {
  product: number;
  product_name?: string;
  quantity: number;
  discounted_price?: number;
}

export interface Order {
  orderid: number;
  ord_date: string;
  supermarket: number;
  distributor: string;
  distributor_name?: string;
  items?: OrderItem[];
  item_data?: { product: number; quantity: number }[];
  calculated_total?: number;
}

export interface Me {
  enumber: number;
  name: string;
  role: string;
  group: string;
  supermarket_id: number;
  supermarket_location: string;
  salary?: number;
  age?: number;
  contact?: string;
  sex?: string;
  supervisor_name?: string | null;
}

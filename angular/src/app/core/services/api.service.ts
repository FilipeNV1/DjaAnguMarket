import { environment } from '../../../environments/environment';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import {
  Supermarket, Section, Employee, Product, Warehouse,
  Distributor, Client, Purchase, Order,
} from '../models';

const BASE = environment.apiUrl;

@Injectable({ providedIn: 'root' })
export class ApiService {
  constructor(private http: HttpClient) {}

  // Supermarkets
  getSupermarkets(): Observable<Supermarket[]> { return this.http.get<Supermarket[]>(`${BASE}/supermarkets/`); }
  getSupermarket(id: number): Observable<Supermarket> { return this.http.get<Supermarket>(`${BASE}/supermarkets/${id}/`); }
  createSupermarket(data: any): Observable<Supermarket> { return this.http.post<Supermarket>(`${BASE}/supermarkets/`, data); }
  updateSupermarket(id: number, data: any): Observable<Supermarket> { return this.http.put<Supermarket>(`${BASE}/supermarkets/${id}/`, data); }
  deleteSupermarket(id: number): Observable<void> { return this.http.delete<void>(`${BASE}/supermarkets/${id}/`); }

  // Sections
  getSections(): Observable<Section[]> { return this.http.get<Section[]>(`${BASE}/sections/`); }
  getSection(sname: string): Observable<Section> { return this.http.get<Section>(`${BASE}/sections/${encodeURIComponent(sname)}/`); }
  createSection(data: any): Observable<Section> { return this.http.post<Section>(`${BASE}/sections/`, data); }
  updateSection(sname: string, data: any): Observable<Section> { return this.http.put<Section>(`${BASE}/sections/${encodeURIComponent(sname)}/`, data); }
  deleteSection(sname: string): Observable<void> { return this.http.delete<void>(`${BASE}/sections/${encodeURIComponent(sname)}/`); }

  // Employees
  getEmployees(): Observable<Employee[]> { return this.http.get<Employee[]>(`${BASE}/employees/`); }
  getEmployee(enumber: number): Observable<Employee> { return this.http.get<Employee>(`${BASE}/employees/${enumber}/`); }
  createEmployee(data: any): Observable<Employee> { return this.http.post<Employee>(`${BASE}/employees/`, data); }
  updateEmployee(enumber: number, data: any): Observable<Employee> { return this.http.put<Employee>(`${BASE}/employees/${enumber}/`, data); }
  deleteEmployee(enumber: number): Observable<void> { return this.http.delete<void>(`${BASE}/employees/${enumber}/`); }

  // Products
  getProducts(): Observable<Product[]> { return this.http.get<Product[]>(`${BASE}/products/`); }
  getProduct(id: number): Observable<Product> { return this.http.get<Product>(`${BASE}/products/${id}/`); }
  createProduct(data: any): Observable<Product> { return this.http.post<Product>(`${BASE}/products/`, data); }
  updateProduct(id: number, data: any): Observable<Product> { return this.http.put<Product>(`${BASE}/products/${id}/`, data); }
  deleteProduct(id: number): Observable<void> { return this.http.delete<void>(`${BASE}/products/${id}/`); }

  // Warehouses
  getWarehouses(): Observable<Warehouse[]> { return this.http.get<Warehouse[]>(`${BASE}/warehouses/`); }
  getWarehouse(id: number): Observable<Warehouse> { return this.http.get<Warehouse>(`${BASE}/warehouses/${id}/`); }
  createWarehouse(data: any): Observable<Warehouse> { return this.http.post<Warehouse>(`${BASE}/warehouses/`, data); }
  updateWarehouse(id: number, data: any): Observable<Warehouse> { return this.http.put<Warehouse>(`${BASE}/warehouses/${id}/`, data); }
  deleteWarehouse(id: number): Observable<void> { return this.http.delete<void>(`${BASE}/warehouses/${id}/`); }

  // Distributors
  getDistributors(): Observable<Distributor[]> { return this.http.get<Distributor[]>(`${BASE}/distributors/`); }
  getDistributor(email: string): Observable<Distributor> { return this.http.get<Distributor>(`${BASE}/distributors/${encodeURIComponent(email)}/`); }
  createDistributor(data: any): Observable<Distributor> { return this.http.post<Distributor>(`${BASE}/distributors/`, data); }
  updateDistributor(email: string, data: any): Observable<Distributor> { return this.http.put<Distributor>(`${BASE}/distributors/${encodeURIComponent(email)}/`, data); }
  deleteDistributor(email: string): Observable<void> { return this.http.delete<void>(`${BASE}/distributors/${encodeURIComponent(email)}/`); }

  // Clients
  getClients(): Observable<Client[]> { return this.http.get<Client[]>(`${BASE}/clients/`); }
  getClient(nif: number): Observable<Client> { return this.http.get<Client>(`${BASE}/clients/${nif}/`); }
  createClient(data: any): Observable<Client> { return this.http.post<Client>(`${BASE}/clients/`, data); }
  updateClient(nif: number, data: any): Observable<Client> { return this.http.put<Client>(`${BASE}/clients/${nif}/`, data); }
  deleteClient(nif: number): Observable<void> { return this.http.delete<void>(`${BASE}/clients/${nif}/`); }

  // Purchases
  getPurchases(): Observable<Purchase[]> { return this.http.get<Purchase[]>(`${BASE}/purchases/`); }
  getPurchase(id: number): Observable<Purchase> { return this.http.get<Purchase>(`${BASE}/purchases/${id}/`); }
  createPurchase(data: any): Observable<Purchase> { return this.http.post<Purchase>(`${BASE}/purchases/`, data); }
  updatePurchase(id: number, data: any): Observable<Purchase> { return this.http.put<Purchase>(`${BASE}/purchases/${id}/`, data); }
  deletePurchase(id: number): Observable<void> { return this.http.delete<void>(`${BASE}/purchases/${id}/`); }

  // Orders
  getOrders(): Observable<Order[]> { return this.http.get<Order[]>(`${BASE}/orders/`); }
  getOrder(id: number): Observable<Order> { return this.http.get<Order>(`${BASE}/orders/${id}/`); }
  createOrder(data: any): Observable<Order> { return this.http.post<Order>(`${BASE}/orders/`, data); }
  updateOrder(id: number, data: any): Observable<Order> { return this.http.put<Order>(`${BASE}/orders/${id}/`, data); }
  deleteOrder(id: number): Observable<void> { return this.http.delete<void>(`${BASE}/orders/${id}/`); }
}

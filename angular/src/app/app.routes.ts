import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  { path: 'login', loadComponent: () => import('./features/auth/login/login').then(m => m.LoginComponent) },
  {
    path: '',
    canActivate: [authGuard],
    children: [
      { path: '', loadComponent: () => import('./features/home/home').then(m => m.HomeComponent) },
      { path: 'profile', loadComponent: () => import('./features/profile/profile').then(m => m.ProfileComponent) },

      { path: 'supermarkets', loadComponent: () => import('./features/supermarkets/supermarket-list/supermarket-list').then(m => m.SupermarketListComponent) },
      { path: 'supermarkets/new', loadComponent: () => import('./features/supermarkets/supermarket-form/supermarket-form').then(m => m.SupermarketFormComponent) },
      { path: 'supermarkets/:id', loadComponent: () => import('./features/supermarkets/supermarket-detail/supermarket-detail').then(m => m.SupermarketDetailComponent) },
      { path: 'supermarkets/:id/edit', loadComponent: () => import('./features/supermarkets/supermarket-form/supermarket-form').then(m => m.SupermarketFormComponent) },

      { path: 'sections', loadComponent: () => import('./features/sections/section-list/section-list').then(m => m.SectionListComponent) },
      { path: 'sections/new', loadComponent: () => import('./features/sections/section-form/section-form').then(m => m.SectionFormComponent) },
      { path: 'sections/:id', loadComponent: () => import('./features/sections/section-detail/section-detail').then(m => m.SectionDetailComponent) },
      { path: 'sections/:id/edit', loadComponent: () => import('./features/sections/section-form/section-form').then(m => m.SectionFormComponent) },

      { path: 'employees', loadComponent: () => import('./features/employees/employee-list/employee-list').then(m => m.EmployeeListComponent) },
      { path: 'employees/new', loadComponent: () => import('./features/employees/employee-form/employee-form').then(m => m.EmployeeFormComponent) },
      { path: 'employees/:id', loadComponent: () => import('./features/employees/employee-detail/employee-detail').then(m => m.EmployeeDetailComponent) },
      { path: 'employees/:id/edit', loadComponent: () => import('./features/employees/employee-form/employee-form').then(m => m.EmployeeFormComponent) },

      { path: 'products', loadComponent: () => import('./features/products/product-list/product-list').then(m => m.ProductListComponent) },
      { path: 'products/new', loadComponent: () => import('./features/products/product-form/product-form').then(m => m.ProductFormComponent) },
      { path: 'products/:id', loadComponent: () => import('./features/products/product-detail/product-detail').then(m => m.ProductDetailComponent) },
      { path: 'products/:id/edit', loadComponent: () => import('./features/products/product-form/product-form').then(m => m.ProductFormComponent) },

      { path: 'warehouses', loadComponent: () => import('./features/warehouses/warehouse-list/warehouse-list').then(m => m.WarehouseListComponent) },
      { path: 'warehouses/new', loadComponent: () => import('./features/warehouses/warehouse-form/warehouse-form').then(m => m.WarehouseFormComponent) },
      { path: 'warehouses/:id', loadComponent: () => import('./features/warehouses/warehouse-detail/warehouse-detail').then(m => m.WarehouseDetailComponent) },
      { path: 'warehouses/:id/edit', loadComponent: () => import('./features/warehouses/warehouse-form/warehouse-form').then(m => m.WarehouseFormComponent) },

      { path: 'distributors', loadComponent: () => import('./features/distributors/distributor-list/distributor-list').then(m => m.DistributorListComponent) },
      { path: 'distributors/new', loadComponent: () => import('./features/distributors/distributor-form/distributor-form').then(m => m.DistributorFormComponent) },
      { path: 'distributors/:id', loadComponent: () => import('./features/distributors/distributor-detail/distributor-detail').then(m => m.DistributorDetailComponent) },
      { path: 'distributors/:id/edit', loadComponent: () => import('./features/distributors/distributor-form/distributor-form').then(m => m.DistributorFormComponent) },

      { path: 'clients', loadComponent: () => import('./features/clients/client-list/client-list').then(m => m.ClientListComponent) },
      { path: 'clients/new', loadComponent: () => import('./features/clients/client-form/client-form').then(m => m.ClientFormComponent) },
      { path: 'clients/:id', loadComponent: () => import('./features/clients/client-detail/client-detail').then(m => m.ClientDetailComponent) },
      { path: 'clients/:id/edit', loadComponent: () => import('./features/clients/client-form/client-form').then(m => m.ClientFormComponent) },

      { path: 'purchases', loadComponent: () => import('./features/purchases/purchase-list/purchase-list').then(m => m.PurchaseListComponent) },
      { path: 'purchases/new', loadComponent: () => import('./features/purchases/purchase-form/purchase-form').then(m => m.PurchaseFormComponent) },
      { path: 'purchases/:id', loadComponent: () => import('./features/purchases/purchase-detail/purchase-detail').then(m => m.PurchaseDetailComponent) },
      { path: 'purchases/:id/edit', loadComponent: () => import('./features/purchases/purchase-form/purchase-form').then(m => m.PurchaseFormComponent) },

      { path: 'orders', loadComponent: () => import('./features/orders/order-list/order-list').then(m => m.OrderListComponent) },
      { path: 'orders/new', loadComponent: () => import('./features/orders/order-form/order-form').then(m => m.OrderFormComponent) },
      { path: 'orders/:id', loadComponent: () => import('./features/orders/order-detail/order-detail').then(m => m.OrderDetailComponent) },
      { path: 'orders/:id/edit', loadComponent: () => import('./features/orders/order-form/order-form').then(m => m.OrderFormComponent) },
    ],
  },
  { path: '**', redirectTo: '' },
];

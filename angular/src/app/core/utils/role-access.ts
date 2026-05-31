export type UserGroup = 'CEO' | 'Manager' | 'Cashier' | 'Employee';

export interface NavItem {
  label: string;
  link: string;
  groups: UserGroup[];
  icon: string;
  description: string;
}

/** Menu entries aligned with Django group permissions. */
export const NAV_ITEMS: NavItem[] = [
  { label: 'Supermarkets', link: '/supermarkets', groups: ['CEO', 'Manager', 'Cashier', 'Employee'], icon: 'bi-buildings', description: 'Manage branches and locations' },
  { label: 'Sections', link: '/sections', groups: ['CEO', 'Manager', 'Cashier', 'Employee'], icon: 'bi-grid-3x3-gap', description: 'Product categories and departments' },
  { label: 'Employees', link: '/employees', groups: ['CEO', 'Manager', 'Cashier', 'Employee'], icon: 'bi-people', description: 'View staff across all locations' },
  { label: 'Products', link: '/products', groups: ['CEO', 'Manager', 'Cashier', 'Employee'], icon: 'bi-box-seam', description: 'Stock, items and sections' },
  { label: 'Warehouses', link: '/warehouses', groups: ['CEO', 'Manager', 'Cashier', 'Employee'], icon: 'bi-building', description: 'Storage locations and inventory' },
  { label: 'Distributors', link: '/distributors', groups: ['CEO', 'Manager', 'Cashier', 'Employee'], icon: 'bi-truck', description: 'Supplier relationships' },
  { label: 'Clients', link: '/clients', groups: ['CEO', 'Manager', 'Cashier', 'Employee'], icon: 'bi-person-badge', description: 'Customer data and fidelity' },
  { label: 'Purchases', link: '/purchases', groups: ['CEO', 'Manager', 'Cashier', 'Employee'], icon: 'bi-receipt', description: 'Transactions and sales' },
  { label: 'Orders', link: '/orders', groups: ['CEO', 'Manager', 'Cashier', 'Employee'], icon: 'bi-bag-check', description: 'Orders from distributors' },
];

export function navItemsForGroup(group: string | null | undefined): NavItem[] {
  if (!group) return [];
  return NAV_ITEMS.filter(item => item.groups.includes(group as UserGroup));
}

export function canAccessRoute(group: string | null | undefined, path: string): boolean {
  return navItemsForGroup(group).some(item => path.startsWith(item.link));
}

export type UserGroup = 'CEO' | 'Manager' | 'Cashier' | 'Employee';

export interface NavItem {
  label: string;
  link: string;
  groups: UserGroup[];
}

/** Menu entries aligned with Django group permissions. */
export const NAV_ITEMS: NavItem[] = [
  { label: 'Supermarkets', link: '/supermarkets', groups: ['CEO', 'Manager', 'Cashier', 'Employee'] },
  { label: 'Sections', link: '/sections', groups: ['CEO', 'Manager', 'Employee'] },
  { label: 'Employees', link: '/employees', groups: ['CEO', 'Manager', 'Employee'] },
  { label: 'Products', link: '/products', groups: ['CEO', 'Manager', 'Cashier', 'Employee'] },
  { label: 'Warehouses', link: '/warehouses', groups: ['CEO', 'Manager', 'Cashier', 'Employee'] },
  { label: 'Distributors', link: '/distributors', groups: ['CEO', 'Manager', 'Employee'] },
  { label: 'Clients', link: '/clients', groups: ['CEO', 'Manager', 'Cashier', 'Employee'] },
  { label: 'Purchases', link: '/purchases', groups: ['CEO', 'Manager', 'Cashier', 'Employee'] },
  { label: 'Orders', link: '/orders', groups: ['CEO', 'Manager', 'Employee'] },
];

export function navItemsForGroup(group: string | null | undefined): NavItem[] {
  if (!group) return [];
  return NAV_ITEMS.filter(item => item.groups.includes(group as UserGroup));
}

export function canAccessRoute(group: string | null | undefined, path: string): boolean {
  return navItemsForGroup(group).some(item => path.startsWith(item.link));
}

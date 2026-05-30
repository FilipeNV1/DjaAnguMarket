import { Me, Employee } from '../models';

/** Build a subtitle without repeating role when it equals the permission group. */
export function userSubtitle(user: Me | Employee): string {
  const parts: string[] = [];
  const role = user.role?.trim();
  const group = user.group?.trim();
  const location = 'supermarket_location' in user ? user.supermarket_location?.trim() : undefined;

  if (role && role !== group) parts.push(role);
  if (group) parts.push(group);
  if (location) parts.push(location);

  return parts.join(' • ');
}

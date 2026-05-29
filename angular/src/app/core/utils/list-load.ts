import { Observable } from 'rxjs';

export const LIST_LOAD_ERROR = 'Could not load data. Make sure Django is running and you are logged in.';

export function loadList<T>(
  fetch: () => Observable<T[]>,
  handlers: {
    onData: (data: T[]) => void;
    onLoading: (loading: boolean) => void;
    onError: (message: string) => void;
  },
): void {
  handlers.onLoading(true);
  handlers.onError('');
  fetch().subscribe({
    next: data => {
      handlers.onData(data);
      handlers.onLoading(false);
    },
    error: () => {
      handlers.onLoading(false);
      handlers.onError(LIST_LOAD_ERROR);
    },
  });
}

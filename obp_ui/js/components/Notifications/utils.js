import store from '../../store/index';

export function addNotification(notification) {
  store.dispatch('notifications/addNotification', { payload: notification });
}

import { EventBus } from '../eventBus';
import store from '../store';
import { addNotification } from '../components/Notifications/utils';

class ActionHandler {
  constructor() {
    EventBus.$on('action', (action) => {
      this.handleAction(action);
    });
  }

  handleAction(action) {
    switch (action.key) {
      case 'play': {
        this.playerControls({
          do: 'load',
          items: [{
            ct: action.ct,
            uuid: action.uuid,
          }],
        });
        break;
      }
      case 'queue': {
        this.playerControls({
          do: 'load',
          opts: {
            mode: 'queue',
          },
          items: [{
            ct: action.ct,
            uuid: action.uuid,
          }],
        });
        break;
      }
      case 'download': {
        const objectKeys = [`${action.ct}:${action.uuid}`];
        store.dispatch('exporter/createExport', { objectKeys });
        break;
      }
      case 'schedule': {
        const co = {
          name: '...loading...',
          ct: action.ct,
          uuid: action.uuid,
          url: action.url,
        };
        store.dispatch('scheduler/addToClipboard', co);
        addNotification({
          title: 'Added to Clipboard',
          body: 'You now will fnid this broadcast in the <a href="/program/scheduler/">scheduler</a>.',
          lifetime: 5000,
        });
        break;
      }
      default: {
        if (action.url) {
          document.location.href = action.url;
        }
      }
    }
  }

  // eslint-disable-next-line class-methods-use-this
  playerControls(action) {
    const e = new CustomEvent('player:controls', { detail: action });
    window.dispatchEvent(e);
  }
}

const instance = new ActionHandler();
export { instance as ActionHandler };

import { EventBus } from '../eventBus';
import store from '../store';

class ActionHandler {
  constructor() {
    EventBus.$on('action', (action) => {
      this.handleAction(action);
    });
  }

  handleAction(action) {
    // console.debug('handleAction', action);

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
      case 'schedule': {
        const co = {
          name: '...loading...',
          ct: action.ct,
          uuid: action.uuid,
          url: action.url,
        };
        store.dispatch('scheduler/addToClipboard', co);
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

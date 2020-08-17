import soundmanager from 'soundmanager2/script/soundmanager2-html5';
import store from '../../store';

const DEBUG = true;

class PlayerBackend {
  constructor(opts) {
    this.player = null;
    soundManager.setup({
      forceUseGlobalHTML5Audio: true,
      html5PollingInterval: 100,
      debugMode: true,
      onready: () => {
        this.player = soundManager.createSound({
          multiShot: false,
          id: 'player_backend_sm2',
        });
      },
    });
  }
}

export default PlayerBackend;

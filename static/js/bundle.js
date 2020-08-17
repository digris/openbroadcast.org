// legacy stylesheet imports
import '../sass/screen.sass';
import '../sass/scheduler.sass';

// global stylesheet import
import '../style/main.scss';

// site apps
import AppInitializer from './initializer';

// icon set & fonts
require('../font/icons.font');

// $((e) => {
document.addEventListener('DOMContentLoaded', () => {
  // initializer has to wait for dom ready, as
  // vue apps need container to mount
  // eslint-disable-next-line no-new
  new AppInitializer();
});

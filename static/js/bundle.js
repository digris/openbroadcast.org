// legacy stylesheet imports
import '../sass/screen.sass'
import '../sass/scheduler.sass'

// global stylesheet import
import '../sass/bundle.sass';

// site apps
import AppInitializer from './initializer'

const DEBUG = true;

$((e) => {
    // initializer has to wait for dom ready, as
    // vue apps need container to mount
    const initializer = new AppInitializer({});
});


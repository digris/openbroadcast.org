// legacy stylesheet imports
// import '../sass/screen.sass'
// import '../sass/scheduler.sass'

// global stylesheet import
import '../style/main.scss';

// site apps
import AppInitializer from './initializer'

const DEBUG = true;

// $((e) => {
document.addEventListener("DOMContentLoaded", () => {
    // initializer has to wait for dom ready, as
    // vue apps need container to mount
    const initializer = new AppInitializer({});
});


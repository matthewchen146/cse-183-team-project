import App from './components/App.js'
import test from './components/Test.js'

let app;

async function init() {

    const { createApp } = Vue;

    console.log(App)

    app = createApp(App);

    app.mount('#vue-target');
}

init();
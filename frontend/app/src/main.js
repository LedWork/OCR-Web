import { createApp } from 'vue'
import { BootstrapVue3 } from 'bootstrap-vue-3';
import App from './App.vue'
import router from './router'
import './assets/scss/custom.scss';
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

const app = createApp(App)

app.use(router)
app.use(BootstrapVue3);

app.mount('#app')

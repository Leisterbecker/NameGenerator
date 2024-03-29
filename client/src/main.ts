import { createApp } from 'vue'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config';

import App from './App.vue'
import router from './router'

import "./assets/main.css";
import "primevue/resources/primevue.min.css"
import "primevue/resources/themes/bootstrap4-light-purple/theme.css"



const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(PrimeVue)

app.mount('#app')

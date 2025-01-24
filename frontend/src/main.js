// main.js
import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";

const pinia = createPinia(); // Crea la instancia de Pinia
const app = createApp(App);

app.use(pinia); // Asegúrate de usar Pinia
app.use(router); // Asegúrate de usar el router
app.mount("#app"); // Monta la aplicación
import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue'; // Importamos la vista de Login
import Reservas from '../views/Reservas.vue'; // Vista para usuarios normales
import Administrar from '../views/Administrar.vue'; // Vista principal del administrador
import UsuariosAdmin from '../views/UsuariosAdmin.vue'; // Vista para gestión de usuarios
import EstadisticasAdmin from '../views/EstadisticasAdmin.vue'; // Vista para estadísticas de reservas

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login, // Ruta principal será Login
  },
  {
    path: '/reservas',
    name: 'Reservas',
    component: Reservas, // Vista para usuarios normales
  },
  {
    path: '/administrar',
    name: 'Administrar',
    component: Administrar, // Vista principal del administrador
  },
  {
    path: '/administrar/usuarios',
    name: 'UsuariosAdmin',
    component: UsuariosAdmin, // Vista para gestión de usuarios
  },
  {
    path: '/administrar/estadisticas',
    name: 'EstadisticasAdmin',
    component: EstadisticasAdmin, // Vista para estadísticas de reservas
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
<template>
    <nav class="navbar-admin">
      <ul class="navbar-list">
        <li>
          <router-link to="/administrar" active-class="active-link">Inicio</router-link>
        </li>
        <li>
          <router-link to="/administrar/usuarios" active-class="active-link">Usuarios</router-link>
        </li>
        <li>
          <router-link to="/administrar/estadisticas" active-class="active-link">Estadísticas</router-link>
        </li>
        <li>
          <button @click="logout">Cerrar sesión</button>
        </li>
      </ul>
    </nav>
  </template>
  
  <script>
  import { useUserStore } from "../stores/userStore";
  import { useRouter } from "vue-router";
  
  export default {
    name: "NavbarAdmin",
    setup() {
      const userStore = useUserStore();
      const router = useRouter();
  
      const logout = () => {
        userStore.clearUsuario();
        router.push("/"); // Redirige al login
      };
  
      return {
        logout,
      };
    },
  };
  </script>
  
  <style scoped>
  .navbar-admin {
    background-color: #007bff;
    color: white;
    padding: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .navbar-list {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    gap: 20px;
  }
  
  .navbar-list li {
    display: inline;
  }
  
  .navbar-list a,
  .navbar-list button {
    color: white;
    text-decoration: none;
    font-weight: bold;
    background: none;
    border: none;
    cursor: pointer;
    padding: 5px 10px;
  }
  
  .navbar-list a.active-link {
    text-decoration: underline;
  }
  
  .navbar-list button:hover,
  .navbar-list a:hover {
    text-decoration: underline;
  }
  </style>
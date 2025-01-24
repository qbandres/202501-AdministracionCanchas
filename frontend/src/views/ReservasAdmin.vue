<template>
  <div>
    <NavbarAdmin />

    <h1>Administrar Reservas</h1>

    <!-- Filtros -->
    <div class="filtros">
      <label for="cancha">Filtrar por Cancha:</label>
      <select id="cancha" v-model="filtroCancha" @change="cargarReservas">
        <option value="">Todas</option>
        <option v-for="cancha in canchas" :key="cancha.id" :value="cancha.id">{{ cancha.nombre }}</option>
      </select>

      <label for="usuario">Filtrar por Usuario:</label>
      <select id="usuario" v-model="filtroUsuario" @change="cargarReservas">
        <option value="">Todos</option>
        <option v-for="usuario in usuarios" :key="usuario.id" :value="usuario.id">{{ usuario.nombre }}</option>
      </select>
    </div>

    <!-- Tabla de Reservas -->
    <table class="reservas-tabla">
      <thead>
        <tr>
          <th>Cancha</th>
          <th>Usuario</th>
          <th>Fecha</th>
          <th>Hora Inicio</th>
          <th>Hora Fin</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="reserva in reservas" :key="reserva.id">
          <td>{{ reserva.cancha_nombre }}</td>
          <td>{{ reserva.usuario_nombre }}</td>
          <td>{{ reserva.fecha_reserva }}</td>
          <td>{{ reserva.hora_inicio }}</td>
          <td>{{ reserva.hora_fin }}</td>
          <td>
            <button @click="editarReserva(reserva)">Editar</button>
            <button @click="eliminarReserva(reserva.id)">Eliminar</button>
          </td>
        </tr>
      </tbody>
    </table>

    <button @click="nuevaReserva">Agregar Reserva</button>
  </div>
</template>

<script>
import axios from "axios";
import NavbarAdmin from "../components/NavbarAdmin.vue";

export default {
  components: { NavbarAdmin },
  data() {
    return {
      reservas: [],
      canchas: [],
      usuarios: [],
      filtroCancha: "",
      filtroUsuario: "",
    };
  },
  methods: {
    async cargarReservas() {
      try {
        const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/reservas`, {
          params: {
            cancha_id: this.filtroCancha || undefined,
            usuario_id: this.filtroUsuario || undefined,
          },
        });
        this.reservas = response.data;
      } catch (error) {
        console.error("Error al cargar reservas:", error);
      }
    },
    async cargarCanchas() {
      const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/canchas`);
      this.canchas = response.data;
    },
    async cargarUsuarios() {
      const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/usuarios`);
      this.usuarios = response.data;
    },
    editarReserva(reserva) {
      // Lógica para editar reserva
    },
    eliminarReserva(id) {
      // Lógica para eliminar reserva
    },
    nuevaReserva() {
      // Lógica para agregar una nueva reserva
    },
  },
  mounted() {
    this.cargarReservas();
    this.cargarCanchas();
    this.cargarUsuarios();
  },
};
</script>

<style scoped>
.filtros {
  margin-bottom: 20px;
  display: flex;
  gap: 20px;
}
.reservas-tabla {
  width: 100%;
  border-collapse: collapse;
}
.reservas-tabla th,
.reservas-tabla td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}
</style>
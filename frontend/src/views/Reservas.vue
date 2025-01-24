<template>
  <div class="reservas-container">
    <h1>Bienvenido, {{ usuario?.nombre }}</h1>

    <!-- Tabla de reservas existentes del usuario -->
    <table v-if="reservasUsuario.length" class="reservas-tabla">
      <thead>
        <tr>
          <th>Cancha</th>
          <th>Fecha</th>
          <th>Hora Inicio</th>
          <th>Hora Fin</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(reserva, index) in reservasUsuario" :key="index">
          <td>{{ reserva.cancha_nombre }}</td>
          <td>{{ reserva.fecha_reserva }}</td>
          <td>{{ reserva.hora_inicio }}</td>
          <td>{{ reserva.hora_fin }}</td>
          <td>
            <button @click="confirmarEliminacion(reserva.id)">Eliminar</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Formulario para seleccionar cancha y fecha -->
    <form @submit.prevent="buscarHorarios">
      <div class="form-group">
        <label for="cancha">Seleccionar Cancha:</label>
        <select v-model="canchaSeleccionada" id="cancha" required @change="cargarHorariosSiListo">
          <option value="" disabled>Seleccione una cancha</option>
          <option v-for="cancha in canchas" :key="cancha.id" :value="cancha.id">
            {{ cancha.nombre }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="fecha">Seleccionar Fecha:</label>
        <input type="date" v-model="fechaSeleccionada" id="fecha" required @change="cargarHorariosSiListo" />
      </div>
    </form>

    <!-- Horarios disponibles -->
    <div v-if="horarios.length > 0" class="horarios-container">
      <h2>Horarios Disponibles para el {{ fechaSeleccionada }}</h2>
      <ul>
        <li v-for="(horario, index) in horarios" :key="index">
          {{ horario[0] }} - {{ horario[1] }}
          <button @click="reservarHorario(horario)">Reservar</button>
        </li>
      </ul>
    </div>

    <!-- Mensaje flotante -->
    <div v-if="mensaje" :class="['mensaje-flotante', { error: mensajeError, success: !mensajeError }]">
      {{ mensaje }}
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useUserStore } from "../stores/userStore";

export default {
  data() {
    return {
      canchas: [], // Lista de canchas disponibles
      canchaSeleccionada: null,
      fechaSeleccionada: "",
      horarios: [], // Horarios disponibles
      reservasUsuario: [], // Reservas del usuario
      mensaje: "", // Mensaje de éxito o error
      mensajeError: false, // Flag para identificar si el mensaje es de error
    };
  },
  computed: {
    usuario() {
      const userStore = useUserStore();
      return userStore.usuario; // Accede al usuario desde el store
    },
  },
  mounted() {
    if (!this.usuario) {
      this.$router.push("/"); // Redirige si no hay usuario logueado
      return;
    }
    this.cargarCanchas();
    this.cargarReservasUsuario();
  },
  methods: {
    async cargarCanchas() {
      try {
        const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/canchas`);
        this.canchas = response.data;
      } catch (error) {
        this.mostrarMensaje("Error al cargar las canchas.", true);
      }
    },
    async buscarHorarios() {
      try {
        const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/reservas/disponibilidad/`, {
          params: {
            cancha_id: this.canchaSeleccionada,
            fecha: this.fechaSeleccionada,
          },
        });
        this.horarios = response.data.horarios_disponibles;
        this.mensaje = ""; // Limpia cualquier mensaje previo
      } catch (error) {
        this.mostrarMensaje("Error al buscar los horarios. Inténtalo nuevamente.", true);
      }
    },
    async reservarHorario(horario) {
      try {
        const payload = {
          usuario_id: this.usuario.id, // Obtiene el ID del usuario desde el store
          cancha_id: this.canchaSeleccionada,
          fecha_reserva: this.fechaSeleccionada,
          hora_inicio: horario[0],
          hora_fin: horario[1],
        };

        await axios.post(`${import.meta.env.VITE_BACKEND_URL}/reservas`, payload);

        // Muestra el mensaje de éxito inmediatamente
        this.mostrarMensaje("Reserva confirmada.", false);

        // Actualiza las reservas del usuario y los horarios disponibles
        await this.cargarReservasUsuario();
        await this.buscarHorarios();
      } catch (error) {
        const mensajeError = error.response?.data?.detail || "Error al realizar la reserva.";
        this.mostrarMensaje(mensajeError, true);
      }
    },
    confirmarEliminacion(id) {
      if (confirm("¿Estás seguro de que deseas eliminar esta reserva?")) {
        this.eliminarReserva(id);
      }
    },
    async eliminarReserva(id) {
      try {
        await axios.delete(`${import.meta.env.VITE_BACKEND_URL}/reservas/${id}`);
        this.mostrarMensaje("Reserva eliminada correctamente.", false);
        await this.cargarReservasUsuario(); // Actualizar reservas del usuario
      } catch (error) {
        this.mostrarMensaje("Error al eliminar la reserva.", true);
      }
    },
    mostrarMensaje(mensaje, esError) {
      this.mensaje = mensaje;
      this.mensajeError = esError;
      setTimeout(() => {
        this.mensaje = "";
      }, 3000); // Mensaje desaparece tras 3 segundos
    },
    cargarHorariosSiListo() {
      if (this.canchaSeleccionada && this.fechaSeleccionada) {
        this.buscarHorarios();
      }
    },
    async cargarReservasUsuario() {
      try {
        console.log("Cargando reservas para usuario ID:", this.usuario.id); // Verifica el ID en la consola
        const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/reservas`, {
          params: { usuario_id: this.usuario.id }, // Obtiene el ID desde el store
        });
        this.reservasUsuario = response.data
          .map(reserva => ({
            ...reserva,
            cancha_nombre: this.canchas.find(cancha => cancha.id === reserva.cancha_id)?.nombre || "Desconocida",
          }))
          .sort((a, b) => new Date(a.fecha_reserva) - new Date(b.fecha_reserva));
      } catch (error) {
        this.mostrarMensaje("Error al cargar tus reservas.", true);
      }
    },
  },
};
</script>

<style scoped>
.reservas-container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
.form-group {
  margin-bottom: 15px;
}
.horarios-container {
  margin-top: 20px;
}
.mensaje-flotante {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 10px 20px;
  border-radius: 5px;
  color: white;
  font-weight: bold;
  z-index: 9999;
  animation: fade-in 0.5s ease-in-out, fade-out 0.5s ease-in-out 2.5s;
}
.mensaje-flotante.success {
  background-color: green;
}
.mensaje-flotante.error {
  background-color: red;
}
.reservas-tabla {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}
.reservas-tabla th,
.reservas-tabla td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}
.reservas-tabla th {
  background-color: #f2f2f2;
}
@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
@keyframes fade-out {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}
</style>
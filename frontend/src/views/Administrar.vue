<template>
  <div>
    <NavbarAdmin /> <!-- Navbar visible en todas las vistas -->

    <div class="admin-container">
      <h1>Administrar Reservas</h1>

      <!-- Filtros -->
      <div class="filtros-container">
        <div class="form-group">
          <label for="filtroCancha">Filtrar por Cancha:</label>
          <select v-model="filtroCancha" id="filtroCancha">
            <option value="">Todas las Canchas</option>
            <option v-for="cancha in canchas" :key="cancha.id" :value="cancha.id">
              {{ cancha.nombre }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="filtroUsuario">Filtrar por Usuario:</label>
          <select v-model="filtroUsuario" id="filtroUsuario">
            <option value="">Todos los Usuarios</option>
            <option v-for="usuario in usuarios" :key="usuario.id" :value="usuario.id">
              {{ usuario.nombre }}
            </option>
          </select>
        </div>
      </div>

      <!-- Tabla de Reservas -->
      <table class="reservas-tabla">
        <thead>
          <tr>
            <th>Cancha</th>
            <th>Nombre</th>
            <th>Teléfono</th>
            <th>Fecha</th>
            <th>Hora Inicio</th>
            <th>Hora Fin</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(reserva, index) in reservasFiltradas" :key="index">
            <td>{{ reserva.cancha_nombre }}</td>
            <td>{{ reserva.usuario_nombre }}</td>
            <td>{{ reserva.usuario_telefono }}</td>
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

      <!-- Botón para agregar una nueva reserva -->
      <button @click="mostrarFormularioAgregar">Agregar Reserva</button>

      <!-- Formulario para agregar o editar reservas -->
      <div v-if="mostrandoFormulario" class="formulario-container">
        <h2>{{ reservaSeleccionada ? "Editar Reserva" : "Agregar Reserva" }}</h2>
        <form @submit.prevent="procesarFormulario">
          <div class="form-group">
            <label for="cancha">Cancha:</label>
            <select v-model="formularioReserva.cancha_id" id="cancha" required>
              <option value="" disabled>Seleccione una cancha</option>
              <option v-for="cancha in canchas" :key="cancha.id" :value="cancha.id">
                {{ cancha.nombre }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="usuario">Usuario:</label>
            <select v-model="formularioReserva.usuario_id" id="usuario" @change="cargarTelefonoUsuario" required>
              <option value="" disabled>Seleccione un usuario</option>
              <option v-for="usuario in usuarios" :key="usuario.id" :value="usuario.id">
                {{ usuario.nombre }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="telefono">Teléfono:</label>
            <input type="text" id="telefono" :value="telefonoSeleccionado" disabled />
          </div>
          <div class="form-group">
            <label for="fecha">Fecha:</label>
            <input type="date" v-model="formularioReserva.fecha_reserva" id="fecha" @change="cargarHorariosDisponibles" required />
          </div>
          <div class="form-group">
            <label>Horarios Disponibles:</label>
            <div class="horarios-disponibles">
              <button
                v-for="(horario, index) in horariosDisponibles"
                :key="index"
                type="button"
                @click="seleccionarHorario(horario)"
              >
                {{ horario[0] }} - {{ horario[1] }}
              </button>
            </div>
          </div>
          <div v-if="formularioReserva.hora_inicio && formularioReserva.hora_fin" class="form-group">
            <p><strong>Hora Inicio:</strong> {{ formularioReserva.hora_inicio }}</p>
            <p><strong>Hora Fin:</strong> {{ formularioReserva.hora_fin }}</p>
          </div>
          <button type="submit">{{ reservaSeleccionada ? "Guardar Cambios" : "Agregar" }}</button>
          <button type="button" @click="cancelarFormulario">Cancelar</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import NavbarAdmin from "../components/NavbarAdmin.vue";

export default {
  components: {
    NavbarAdmin,
  },
  data() {
    return {
      reservas: [],
      canchas: [],
      usuarios: [],
      horariosDisponibles: [],
      telefonoSeleccionado: "",
      mostrandoFormulario: false,
      reservaSeleccionada: null,
      filtroCancha: "",
      filtroUsuario: "",
      formularioReserva: {
        cancha_id: "",
        usuario_id: "",
        fecha_reserva: "",
        hora_inicio: "",
        hora_fin: "",
      },
    };
  },
  computed: {
    reservasFiltradas() {
      return this.reservas.filter((reserva) => {
        const coincideCancha = this.filtroCancha ? reserva.cancha_id === this.filtroCancha : true;
        const coincideUsuario = this.filtroUsuario ? reserva.usuario_id === this.filtroUsuario : true;
        return coincideCancha && coincideUsuario;
      });
    },
  },
  methods: {
    async cargarReservas() {
      try {
        const reservasResponse = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/reservas`);
        const usuariosResponse = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/usuarios`);

        const usuarios = usuariosResponse.data;

        this.reservas = reservasResponse.data.map((reserva) => {
          const usuario = usuarios.find((u) => u.id === reserva.usuario_id);
          const cancha = this.canchas.find((c) => c.id === reserva.cancha_id);

          return {
            ...reserva,
            cancha_nombre: cancha ? cancha.nombre : "Cancha Desconocida",
            usuario_nombre: usuario ? usuario.nombre : "Usuario Desconocido",
            usuario_telefono: usuario ? usuario.telefono : "Teléfono no disponible",
          };
        });
      } catch (error) {
        console.error("Error al cargar las reservas:", error);
      }
    },
    async cargarCanchas() {
      try {
        const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/canchas`);
        this.canchas = response.data;
      } catch (error) {
        console.error("Error al cargar las canchas:", error);
      }
    },
    async cargarUsuarios() {
      try {
        const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/usuarios`);
        this.usuarios = response.data;
      } catch (error) {
        console.error("Error al cargar los usuarios:", error);
      }
    },
    async cargarHorariosDisponibles() {
      if (this.formularioReserva.cancha_id && this.formularioReserva.fecha_reserva) {
        try {
          const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/reservas/disponibilidad/`, {
            params: {
              cancha_id: this.formularioReserva.cancha_id,
              fecha: this.formularioReserva.fecha_reserva,
            },
          });
          this.horariosDisponibles = response.data.horarios_disponibles;
        } catch (error) {
          console.error("Error al cargar los horarios disponibles:", error);
        }
      }
    },
    cargarTelefonoUsuario() {
      const usuario = this.usuarios.find((u) => u.id === this.formularioReserva.usuario_id);
      this.telefonoSeleccionado = usuario ? usuario.telefono : "";
    },
    mostrarFormularioAgregar() {
      this.mostrandoFormulario = true;
      this.reservaSeleccionada = null;
      this.formularioReserva = {
        cancha_id: "",
        usuario_id: "",
        fecha_reserva: "",
        hora_inicio: "",
        hora_fin: "",
      };
      this.telefonoSeleccionado = "";
      this.horariosDisponibles = [];
    },
    seleccionarHorario(horario) {
      this.formularioReserva.hora_inicio = horario[0];
      this.formularioReserva.hora_fin = horario[1];
    },
    editarReserva(reserva) {
      this.mostrandoFormulario = true;
      this.reservaSeleccionada = reserva;
      this.formularioReserva = { ...reserva };
      this.cargarHorariosDisponibles();
      this.cargarTelefonoUsuario();
    },
    async procesarFormulario() {
      try {
        if (this.reservaSeleccionada) {
          await axios.put(
            `${import.meta.env.VITE_BACKEND_URL}/reservas/${this.reservaSeleccionada.id}`,
            this.formularioReserva
          );
        } else {
          await axios.post(`${import.meta.env.VITE_BACKEND_URL}/reservas/admin/`, this.formularioReserva);
        }
        this.cargarReservas();
        this.mostrandoFormulario = false;
      } catch (error) {
        console.error("Error al procesar el formulario:", error);
      }
    },
    async eliminarReserva(id) {
      try {
        await axios.delete(`${import.meta.env.VITE_BACKEND_URL}/reservas/${id}`);
        this.cargarReservas();
      } catch (error) {
        console.error("Error al eliminar la reserva:", error);
      }
    },
    cancelarFormulario() {
      this.mostrandoFormulario = false;
    },
  },
  watch: {
    "formularioReserva.cancha_id": "cargarHorariosDisponibles",
    "formularioReserva.fecha_reserva": "cargarHorariosDisponibles",
  },
  mounted() {
    this.cargarReservas();
    this.cargarCanchas();
    this.cargarUsuarios();
  },
};
</script>

<style scoped>
.admin-container {
  padding: 20px;
}
.filtros-container {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
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
.formulario-container {
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #f9f9f9;
}
.form-group {
  margin-bottom: 15px;
}
.horarios-disponibles button {
  margin: 5px;
  padding: 5px 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}
.horarios-disponibles button:hover {
  background-color: #0056b3;
}
button {
  margin-right: 10px;
}
</style>
<template>
    <div class="usuarios-admin">
      <h1>GEstion Usuarios</h1>
      <NavbarAdmin />
      <!-- Tabla de usuarios -->
      <table class="usuarios-tabla">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Correo</th>
            <th>Rol</th>
            <th>Teléfono</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="usuario in usuarios" :key="usuario.id">
            <td>{{ usuario.id }}</td>
            <td>{{ usuario.nombre }}</td>
            <td>{{ usuario.correo }}</td>
            <td>{{ usuario.rol }}</td>
            <td>{{ usuario.telefono }}</td>
            <td>
              <button @click="modificarUsuario(usuario)">Modificar</button>
              <button @click="eliminarUsuario(usuario.id)">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
      <!-- Botón para agregar usuario -->
      <button @click="abrirFormularioAgregar">Agregar Usuario</button>
  
      <!-- Formulario para agregar/modificar usuarios -->
      <div v-if="mostrarFormulario" class="formulario-usuario">
        <h2>{{ usuarioSeleccionado ? 'Modificar Usuario' : 'Agregar Usuario' }}</h2>
        <form @submit.prevent="guardarUsuario">
          <div class="form-group">
            <label>Nombre:</label>
            <input type="text" v-model="usuarioFormulario.nombre" required />
          </div>
          <div class="form-group">
            <label>Correo:</label>
            <input type="email" v-model="usuarioFormulario.correo" required />
          </div>
          <div class="form-group">
            <label>Rol:</label>
            <select v-model="usuarioFormulario.rol" required>
              <option value="usuario">Usuario</option>
              <option value="admin">Administrador</option>
            </select>
          </div>
          <div class="form-group">
            <label>Teléfono:</label>
            <input type="text" v-model="usuarioFormulario.telefono" />
          </div>
          <div class="form-group">
            <label>Contraseña:</label>
            <input type="password" v-model="usuarioFormulario.password" :required="!usuarioSeleccionado" />
          </div>
          <button type="submit">{{ usuarioSeleccionado ? 'Actualizar' : 'Agregar' }}</button>
          <button @click="cerrarFormulario">Cancelar</button>
        </form>
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
        usuarios: [], // Lista de usuarios
        mostrarFormulario: false, // Muestra/oculta el formulario
        usuarioFormulario: {
          nombre: "",
          correo: "",
          rol: "usuario",
          telefono: "",
          password: "",
        },
        usuarioSeleccionado: null, // Usuario seleccionado para modificar
      };
    },
    methods: {
      async cargarUsuarios() {
        try {
          const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/usuarios`);
          this.usuarios = response.data;
        } catch (error) {
          console.error("Error al cargar usuarios", error);
        }
      },
      abrirFormularioAgregar() {
        this.mostrarFormulario = true;
        this.usuarioFormulario = {
          nombre: "",
          correo: "",
          rol: "usuario",
          telefono: "",
          password: "",
        };
        this.usuarioSeleccionado = null;
      },
      modificarUsuario(usuario) {
        this.mostrarFormulario = true;
        this.usuarioFormulario = { ...usuario, password: "" }; // No mostrar la contraseña actual
        this.usuarioSeleccionado = usuario;
      },
      async guardarUsuario() {
        try {
          if (this.usuarioSeleccionado) {
            // Actualizar usuario
            await axios.put(`${import.meta.env.VITE_BACKEND_URL}/usuarios/${this.usuarioSeleccionado.id}`, this.usuarioFormulario);
          } else {
            // Agregar nuevo usuario
            await axios.post(`${import.meta.env.VITE_BACKEND_URL}/usuarios`, this.usuarioFormulario);
          }
          this.mostrarFormulario = false;
          this.cargarUsuarios();
        } catch (error) {
          console.error("Error al guardar usuario", error);
        }
      },
      async eliminarUsuario(id) {
        if (confirm("¿Estás seguro de eliminar este usuario?")) {
          try {
            await axios.delete(`${import.meta.env.VITE_BACKEND_URL}/usuarios/${id}`);
            this.cargarUsuarios();
          } catch (error) {
            console.error("Error al eliminar usuario", error);
          }
        }
      },
      cerrarFormulario() {
        this.mostrarFormulario = false;
      },
    },
    mounted() {
      this.cargarUsuarios();
    },
  };
  </script>
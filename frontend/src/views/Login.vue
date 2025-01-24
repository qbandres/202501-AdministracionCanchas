<template>
  <div class="login-container">
    <h1>Iniciar Sesión</h1>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="correo">Correo</label>
        <input
          type="text"
          id="correo"
          v-model="correo"
          placeholder="Correo electrónico"
          required
        />
      </div>
      <div class="form-group">
        <label for="password">Contraseña</label>
        <input
          type="password"
          id="password"
          v-model="password"
          placeholder="Contraseña"
          required
        />
      </div>
      <div v-if="error" class="error-message">{{ error }}</div>
      <button type="submit" :disabled="loading">
        <span v-if="!loading">Iniciar Sesión</span>
        <span v-else>Cargando...</span>
      </button>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import { useUserStore } from "../stores/userStore"; // Importa el store

export default {
  data() {
    return {
      correo: "", // Cambiado de 'usuario' a 'correo'
      password: "",
      error: "",
      loading: false,
    };
  },
  methods: {
    async handleLogin() {
  this.loading = true;
  this.error = "";
  try {
    const response = await axios.post(
      `${import.meta.env.VITE_BACKEND_URL}/login/`,
      {
        correo: this.correo,
        password: this.password,
      }
    );
    console.log("Respuesta del backend:", response.data); // Verifica la respuesta

    const { id, nombre, rol } = response.data;

    // Guarda los datos del usuario en el store
    const userStore = useUserStore();
    userStore.setUsuario({ id, nombre, rol });
    console.log("Usuario guardado en el store:", userStore.usuario);

    this.loading = false;

    if (rol === "admin") {
      this.$router.push("/administrar");
    } else if (rol === "usuario") {
      this.$router.push("/reservas");
    } else {
      throw new Error("Rol desconocido"); // Agrega un caso de error para roles inesperados
    }
  } catch (err) {
    this.loading = false;
    console.error("Error en login:", err.response?.data || err.message);
    this.error =
      err.response && err.response.status === 401
        ? "Usuario o contraseña incorrectos."
        : "Ocurrió un problema. Por favor, inténtalo nuevamente.";
  }
},
  },
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
.form-group {
  margin-bottom: 15px;
}
.error-message {
  color: red;
  margin-bottom: 10px;
}
button {
  background-color: #007bff;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>
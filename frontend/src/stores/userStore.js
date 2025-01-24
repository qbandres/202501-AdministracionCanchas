import { defineStore } from "pinia";

export const useUserStore = defineStore("user", {
  state: () => ({
    usuario: null, // Aquí se guardará el usuario logueado
  }),
  actions: {
    setUsuario(data) {
      this.usuario = data;
    },
    clearUsuario() {
      this.usuario = null;
    },
  },
});
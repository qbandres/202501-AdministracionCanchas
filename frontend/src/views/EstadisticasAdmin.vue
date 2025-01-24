<template>
  <div class="estadisticas-admin">
    <NavbarAdmin /> <!-- Navbar visible en todas las vistas -->

    <h1>Estadísticas de Reservas</h1>

    <!-- Tabla de Historial de Reservas -->
    <table class="estadisticas-tabla">
      <thead>
        <tr>
          <th>Cancha</th>
          <th>Fecha</th>
          <th>Hora Inicio</th>
          <th>Hora Fin</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="reserva in historialReservas" :key="reserva.id">
          <td>{{ reserva.cancha_nombre }}</td>
          <td>{{ reserva.fecha_reserva }}</td>
          <td>{{ reserva.hora_inicio }}</td>
          <td>{{ reserva.hora_fin }}</td>
        </tr>
      </tbody>
    </table>

    <!-- Gráficos -->
    <div class="graficos">
      <h2>Reservas por Día y Cancha</h2>
      <div class="chart-container">
        <canvas id="reservasPorDiaCancha"></canvas>
      </div>

      <h2>Mapa de Horarios más Reservados</h2>
      <div class="chart-container">
        <canvas id="horariosMasReservados"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Chart from "chart.js/auto";
import NavbarAdmin from "../components/NavbarAdmin.vue";

export default {
  components: {
    NavbarAdmin,
  },
  data() {
    return {
      historialReservas: [], // Historial completo de reservas
      canchas: [], // Lista de canchas para mapeo
    };
  },
  methods: {
    async cargarDatos() {
      try {
        // Obtener historial de reservas
        const reservasResponse = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/reservas`);
        const canchasResponse = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/canchas`);
        this.canchas = canchasResponse.data;

        // Mapear historial con nombres de canchas
        this.historialReservas = reservasResponse.data.map((reserva) => {
          const cancha = this.canchas.find((c) => c.id === reserva.cancha_id);
          return {
            ...reserva,
            cancha_nombre: cancha ? cancha.nombre : "Cancha Desconocida",
          };
        });

        this.generarGraficos();
      } catch (error) {
        console.error("Error al cargar los datos", error);
      }
    },
// Parte del método generarGraficos en el script
generarGraficos() {
      // Preparar datos para gráfico de barras
      const reservasPorDiaCancha = {};
      this.historialReservas.forEach((reserva) => {
        const key = `${reserva.fecha_reserva}-${reserva.cancha_nombre}`;
        const horasReservadas =
          new Date(`1970-01-01T${reserva.hora_fin}`).getHours() -
          new Date(`1970-01-01T${reserva.hora_inicio}`).getHours();
        reservasPorDiaCancha[key] = (reservasPorDiaCancha[key] || 0) + horasReservadas;
      });

      const etiquetas = [...new Set(this.historialReservas.map((r) => r.fecha_reserva))];
      const nombresCanchas = [...new Set(this.canchas.map((c) => c.nombre))];
      const datasetHoras = nombresCanchas.map((cancha) => ({
        label: cancha,
        data: etiquetas.map((fecha) => reservasPorDiaCancha[`${fecha}-${cancha}`] || 0),
        backgroundColor: this.generarColorAleatorio(),
      }));

      // Encontrar el valor máximo en los datos para configurar el eje Y dinámicamente
      const valoresMaximos = datasetHoras.map((dataset) =>
        Math.max(...dataset.data)
      );
      const valorMaximoEjeY = Math.max(...valoresMaximos);

      // Gráfico de Barras: Reservas por Día y Cancha
      const ctxDiaCancha = document.getElementById("reservasPorDiaCancha").getContext("2d");
      new Chart(ctxDiaCancha, {
        type: "bar",
        data: {
          labels: etiquetas, // Fechas en el eje X
          datasets: datasetHoras, // Datos de horas reservadas
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: true,
              position: "top",
            },
          },
          scales: {
            x: { title: { display: true, text: "Fecha" } },
            y: {
              title: { display: true, text: "Horas Reservadas" },
              ticks: { stepSize: 1 },
              suggestedMax: valorMaximoEjeY + 1, // Añade un buffer para mejor visibilidad
            },
          },
        },
      });
    },
    generarColorAleatorio() {
      const r = Math.floor(Math.random() * 255);
      const g = Math.floor(Math.random() * 255);
      const b = Math.floor(Math.random() * 255);
      return `rgba(${r}, ${g}, ${b}, 0.6)`;
    },
  },
  mounted() {
    this.cargarDatos();
  },
};
</script>

<style scoped>
.estadisticas-admin {
  padding: 20px;
}
.estadisticas-tabla {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}
.estadisticas-tabla th,
.estadisticas-tabla td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}
.estadisticas-tabla th {
  background-color: #f2f2f2;
}
.graficos {
  margin-top: 20px;
}
.chart-container {
  width: 100%;
  height: 400px;
  margin: 20px 0;
}
canvas {
  width: 100%;
  height: 100%;
}
</style>
document.addEventListener("DOMContentLoaded", async () => {
  const ctx = document.getElementById("trafficChart").getContext("2d");

  try {
    const response = await fetch("http://127.0.0.1:8000/traffic-data");
    const result = await response.json();

    const chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: result.times,
        datasets: [{
          label: 'Traffic Volume',
          data: result.volumes,
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgb(54, 162, 235)',
          borderWidth: 2,
          tension: 0.3
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: { beginAtZero: true }
        }
      }
    });
  } catch (err) {
    console.error("Error loading chart data:", err);
  }
});

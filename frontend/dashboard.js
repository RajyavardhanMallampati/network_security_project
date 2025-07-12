document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.getElementById("fileInput");
  const statusDiv = document.getElementById("status");
  const barChartCanvas = document.getElementById("barChart");
  const pieChartCanvas = document.getElementById("pieChart");
  const table = document.getElementById("resultTable");
  const tableBody = table.querySelector("tbody");

  let barChart, pieChart;

  fileInput.addEventListener("change", async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    statusDiv.textContent = "⏳ Reading and classifying data...";
    tableBody.innerHTML = "";
    table.hidden = false;

    Papa.parse(file, {
      header: true,
      dynamicTyping: true,
      complete: async function (results) {
        const rows = results.data;
        const labelCounts = {};

        for (let i = 0; i < rows.length; i++) {
          const row = rows[i];
          if (!("traffic_type" in row)) continue;

          const payload = {
            traffic_type: row.traffic_type,
            protocol: row.protocol,
            duration: row.duration,
            packet_count: row.packet_count,
            avg_packet_size: row.avg_packet_size,
            bytes_per_sec: row.bytes_per_sec,
            flag: row.flag
          };

          try {
            const res = await fetch("http://127.0.0.1:8000/predict", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(payload)
            });

            const data = await res.json();
            console.log("🧠 Backend Response:", data);

            const className = data.class_name || "Class undefined";
            labelCounts[className] = (labelCounts[className] || 0) + 1;

            const tr = document.createElement("tr");
            tr.innerHTML = `
              <td>${i + 1}</td>
              <td>${row.traffic_type}</td>
              <td>${row.protocol}</td>
              <td>${row.duration}</td>
              <td>${row.packet_count}</td>
              <td>${row.avg_packet_size}</td>
              <td>${row.bytes_per_sec}</td>
              <td>${row.flag}</td>
              <td><span class="badge bg-primary">${className}</span></td>
            `;
            tableBody.appendChild(tr);

          } catch (err) {
            console.error("Prediction failed:", err);
          }
        }

        statusDiv.textContent = "✅ Classification complete.";

        // Update Bar Chart
        const labels = Object.keys(labelCounts);
        const values = Object.values(labelCounts);
        const colors = ['#007bff', '#28a745', '#ffc107', '#17a2b8', '#6f42c1', '#dc3545', '#fd7e14', '#20c997'];

        if (barChart) barChart.destroy();
        barChart = new Chart(barChartCanvas, {
          type: 'bar',
          data: {
            labels,
            datasets: [{
              label: 'Traffic Class Count',
              data: values,
              backgroundColor: colors
            }]
          },
          options: {
            plugins: {
              title: { display: true, text: 'Traffic Class Distribution (Bar)' },
              legend: { display: false },
              tooltip: { mode: 'index', intersect: false }
            },
            responsive: true,
            scales: {
              y: {
                beginAtZero: true,
                title: { display: true, text: 'Count' }
              }
            }
          }
        });

        // Update Pie Chart
        if (pieChart) pieChart.destroy();
        pieChart = new Chart(pieChartCanvas, {
          type: 'pie',
          data: {
            labels,
            datasets: [{
              label: 'Traffic Class',
              data: values,
              backgroundColor: colors
            }]
          },
          options: {
            plugins: {
              title: { display: true, text: 'Traffic Class Distribution (Pie)' }
            },
            responsive: true
          }
        });
      }
    });
  });
});

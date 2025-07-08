const BASE_URL = "http://127.0.0.1:8000";

// Show one section only
function showSection(sectionId) {
  document.querySelectorAll(".section").forEach(sec => sec.classList.remove("active"));
  document.getElementById(sectionId).classList.add("active");

  // Load data when section becomes active
  if (sectionId === "patients") loadPatients();
  else if (sectionId === "doctors") loadDoctors();
  else if (sectionId === "appointments") loadAppointments();
  else if (sectionId === "departments") loadDepartments();
}

// Load Patients
function loadPatients() {
  fetch(`${BASE_URL}/patients/`)
    .then(res => res.json())
    .then(data => {
      const section = document.getElementById("patients");
      section.innerHTML = `
        <h2>👩‍⚕️ Patients</h2>
        <table>
          <tr><th>ID</th><th>Name</th><th>Age</th><th>Condition</th></tr>
          ${data.map(p => `
            <tr>
              <td>${p.id}</td>
              <td>${p.name}</td>
              <td>${p.age}</td>
              <td>${p.condition}</td>
            </tr>
          `).join("")}
        </table>
      `;
    });
}

// Load Doctors
function loadDoctors() {
  fetch(`${BASE_URL}/doctors/`)
    .then(res => res.json())
    .then(data => {
      const section = document.getElementById("doctors");
      section.innerHTML = `
        <h2>👨‍⚕️ Doctors</h2>
        <table>
          <tr><th>ID</th><th>Name</th><th>Specialty</th><th>Experience</th></tr>
          ${data.map(d => `
            <tr>
              <td>${d.id}</td>
              <td>${d.name}</td>
              <td>${d.specialty}</td>
              <td>${d.years_experience}</td>
            </tr>
          `).join("")}
        </table>
      `;
    });
}

// Load Appointments
function loadAppointments() {
  fetch(`${BASE_URL}/appointments/`)
    .then(res => res.json())
    .then(data => {
      const section = document.getElementById("appointments");
      section.innerHTML = `
        <h2>📅 Appointments</h2>
        <table>
          <tr><th>ID</th><th>Patient</th><th>Doctor</th><th>Date</th></tr>
          ${data.map(a => `
            <tr>
              <td>${a.id}</td>
              <td>${a.patient_id}</td>
              <td>${a.doctor_id}</td>
              <td>${a.date}</td>
            </tr>
          `).join("")}
        </table>
      `;
    });
}

// Load Departments
function loadDepartments() {
  fetch(`${BASE_URL}/departments/`)
    .then(res => res.json())
    .then(data => {
      const section = document.getElementById("departments");
      section.innerHTML = `
        <h2>🏢 Departments</h2>
        <table>
          <tr><th>ID</th><th>Name</th><th>Location</th></tr>
          ${data.map(d => `
            <tr>
              <td>${d.id}</td>
              <td>${d.name}</td>
              <td>${d.location}</td>
            </tr>
          `).join("")}
        </table>
      `;
    });
}

// Start with dashboard visible
window.onload = () => showSection('dashboard');

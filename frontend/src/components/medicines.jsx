import React, { useEffect, useState } from "react";
import axios from "axios";

const API = "https://glorious-space-fishstick-pjpgxxpr9qgxc79qp-8000.app.github.dev/medicines"; // Update if port/path differs

function App() {
  const [medicines, setMedicines] = useState([]);
  const [form, setForm] = useState({ name: "", id: null });

  const fetchMedicines = async () => {
    const res = await axios.get(API);
    setMedicines(res.data);
  };

  useEffect(() => {
    fetchMedicines();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (form.id === null) {
      await axios.post(API, { name: form.name });
    } else {
      await axios.put(`${API}/${form.id}`, { name: form.name });
    }
    setForm({ name: "", id: null });
    fetchMedicines();
  };

  const handleEdit = (medicine) => {
    setForm({ name: medicine.name, id: medicine.id });
  };

  const handleDelete = async (id) => {
    await axios.delete(`${API}/${id}`);
    fetchMedicines();
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Medicine Manager</h1>
      <form onSubmit={handleSubmit}>
        <input
          placeholder="Medicine Name"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
        />
        <button type="submit">{form.id === null ? "Add" : "Update"}</button>
      </form>

      <ul>
        {medicines.map((med) => (
          <li key={med.id}>
            {med.name}{" "}
            <button onClick={() => handleEdit(med)}>Edit</button>{" "}
            <button onClick={() => handleDelete(med.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;

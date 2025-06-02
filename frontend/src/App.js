import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Medicines from './components/medicines';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          Welcome to <Link to="/medicines" className="App-link">
            Hospital Management System
          </Link>
        </header>
        <Routes>
          <Route path="/medicines" element={<Medicines />} />
        </Routes>
      </div>
    </Router>
    
  );
}

export default App;

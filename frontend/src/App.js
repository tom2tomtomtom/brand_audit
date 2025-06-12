import React from 'react';
import { Routes, Route } from 'react-router-dom';
import CompetitorWizard from './components/CompetitorWizard';
import './App.css';

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<CompetitorWizard />} />
      </Routes>
    </div>
  );
}

export default App;
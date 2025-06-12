import React, { useState } from 'react';

const CompetitorAnalysisStep = ({ competitors, onSubmit }) => {
  const [selectedCompetitors, setSelectedCompetitors] = useState([]);

  const handleCheckboxChange = (competitor) => {
    if (selectedCompetitors.some(c => c.name === competitor.name)) {
      setSelectedCompetitors(selectedCompetitors.filter(c => c.name !== competitor.name));
    } else {
      setSelectedCompetitors([...selectedCompetitors, competitor]);
    }
  };

  const handleSelectAll = () => {
    if (selectedCompetitors.length === competitors.length) {
      setSelectedCompetitors([]);
    } else {
      setSelectedCompetitors([...competitors]);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (selectedCompetitors.length === 0) {
      alert('Please select at least one competitor to analyze');
      return;
    }
    
    onSubmit(selectedCompetitors);
  };

  return (
    <div>
      <h2 className="mb-4">Select Competitors to Analyze</h2>
      <p className="mb-4">
        We've identified the following potential competitors. Select which ones you'd like to analyze in detail.
      </p>
      
      <div className="card mb-4">
        <div className="card-body">
          <div className="form-check mb-3">
            <input
              type="checkbox"
              className="form-check-input"
              id="select-all"
              checked={selectedCompetitors.length === competitors.length && competitors.length > 0}
              onChange={handleSelectAll}
            />
            <label className="form-check-label fw-bold" htmlFor="select-all">
              {selectedCompetitors.length === competitors.length && competitors.length > 0
                ? 'Deselect All'
                : 'Select All'}
            </label>
          </div>
          
          <div className="list-group">
            {competitors.map((competitor, index) => (
              <div key={index} className="list-group-item">
                <div className="form-check">
                  <input
                    type="checkbox"
                    className="form-check-input"
                    id={`competitor-${index}`}
                    checked={selectedCompetitors.some(c => c.name === competitor.name)}
                    onChange={() => handleCheckboxChange(competitor)}
                  />
                  <label className="form-check-label" htmlFor={`competitor-${index}`}>
                    <strong>{competitor.name}</strong>
                    <div className="text-muted small">{competitor.url}</div>
                  </label>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
      
      <div className="d-flex justify-content-between">
        <div>
          <span className="badge bg-primary me-2">
            {selectedCompetitors.length} selected
          </span>
          <span className="text-muted">
            of {competitors.length} competitors
          </span>
        </div>
        <button
          className="btn btn-primary"
          onClick={handleSubmit}
          disabled={selectedCompetitors.length === 0}
        >
          Analyze Selected Competitors
        </button>
      </div>
    </div>
  );
};

export default CompetitorAnalysisStep;
import React from 'react';
import './LocationSelector.css';

interface LocationSelectorProps {
  onSelectLocation: (location: 'gym' | 'home' | 'home2' | 'back') => void;
}

const LocationSelector: React.FC<LocationSelectorProps> = ({ onSelectLocation }) => {
  return (
    <div className="location-selector">
      <div className="location-container">
        <h1 className="location-title">Was trainierst du heute?</h1>
        <p className="location-subtitle">Wähle deinen Trainingsplan</p>

        <div className="location-buttons">
          <button
            className="location-btn location-btn-gym"
            onClick={() => onSelectLocation('gym')}
          >
            <div className="location-icon">@</div>
            <div className="location-text">
              <span className="location-label">gym</span>
              <span className="location-description">Im Fitnessstudio</span>
            </div>
          </button>

          <button
            className="location-btn location-btn-home"
            onClick={() => onSelectLocation('home')}
          >
            <div className="location-icon">@</div>
            <div className="location-text">
              <span className="location-label">hantel</span>
              <span className="location-description">Hanteltraining</span>
            </div>
          </button>

          <button
            className="location-btn location-btn-home2"
            onClick={() => onSelectLocation('home2')}
          >
            <div className="location-icon">@</div>
            <div className="location-text">
              <span className="location-label">cardio</span>
              <span className="location-description">Cardio Training</span>
            </div>
          </button>

          <button
            className="location-btn location-btn-back"
            onClick={() => onSelectLocation('back')}
          >
            <div className="location-icon">@</div>
            <div className="location-text">
              <span className="location-label">rücken</span>
              <span className="location-description">Rücken-Aufbau & Stabilität</span>
            </div>
          </button>
        </div>
      </div>
    </div>
  );
};

export default LocationSelector;

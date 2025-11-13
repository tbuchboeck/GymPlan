import React from 'react';
import './LocationSelector.css';

interface LocationSelectorProps {
  onSelectLocation: (location: 'gym' | 'home') => void;
}

const LocationSelector: React.FC<LocationSelectorProps> = ({ onSelectLocation }) => {
  return (
    <div className="location-selector">
      <div className="location-container">
        <h1 className="location-title">Wo trainierst du heute?</h1>
        <p className="location-subtitle">Wähle deinen Trainingsort</p>

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
              <span className="location-label">home</span>
              <span className="location-description">Zu Hause</span>
            </div>
          </button>
        </div>
      </div>
    </div>
  );
};

export default LocationSelector;

// frontend/src/components/Plot.js

import React from 'react';

const Plot = ({ src }) => {
  return (
    <div className="plot-container">
      <img src={src} alt="Stock Price Plot" className="plot-image" />
    </div>
  );
};

export default Plot;

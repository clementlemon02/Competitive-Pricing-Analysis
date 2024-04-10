/* eslint-disable prettier/prettier */
import React from 'react'

const Overview = () => {
  const titleStyle = {
    fontSize: '24px', // Custom font size for the title
    fontWeight: 'bold', // Custom font weight for the title
  };

  const subtitleStyle = {
    fontSize: '18px', // Custom font size for the subtitle
    fontStyle: 'italic', // Custom font style for the subtitle
  };

  const textStyle = {
    fontSize: '16px', // Custom font size for the text
  };

  return (
    <div>
      <h1 style={titleStyle}>Overview</h1>

      <h2 style={subtitleStyle}>Project Introduction</h2>

      <p style={textStyle}>
        This is our DSA3101 price optimisation project for Mount Faber cable car.
      </p>
    </div>
  );
};

export default Overview;

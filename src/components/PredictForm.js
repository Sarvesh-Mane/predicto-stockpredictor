import React, { useState } from 'react';
import { TextField, MenuItem, Button, Box } from '@mui/material';

const PredictForm = ({ setPrediction, fetchPlot }) => {
  const [date, setDate] = useState('');
  const [company, setCompany] = useState('AAPL');

  const handlePredict = () => {
    const payload = {
      date: date,
      company: company,
    };

    fetch('http://127.0.0.1:5000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })
      .then((response) => response.json())
      .then((data) => {
        setPrediction(data.prediction);
        fetchPlot(company, date);
      })
      .catch((error) => console.error('Error predicting stock:', error));
  };

  return (
    <Box className="form-container">
      <TextField
        select
        label="Select a Company"
        value={company}
        onChange={(e) => setCompany(e.target.value)}
        fullWidth
        margin="normal"
        variant="outlined"
      >
        <MenuItem value="AAPL">Apple Inc.</MenuItem>
        <MenuItem value="MSFT">Microsoft Corporation</MenuItem>
        <MenuItem value="GOOGL">Alphabet Inc. (Google)</MenuItem>
        <MenuItem value="AMZN">Amazon.com Inc.</MenuItem>
        <MenuItem value="META">Meta Platforms Inc. (Facebook)</MenuItem>
      </TextField>

      <TextField
        label="Select a Date"
        type="date"
        value={date}
        onChange={(e) => setDate(e.target.value)}
        fullWidth
        margin="normal"
        variant="outlined"
        InputLabelProps={{
          shrink: true,
        }}
      />

      <Button variant="contained" color="primary" onClick={handlePredict} fullWidth>
        Predict
      </Button>
    </Box>
  );
};

export default PredictForm;

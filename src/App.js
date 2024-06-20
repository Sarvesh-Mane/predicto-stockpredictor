import React, { useState } from 'react';
import { Container, Grid, Typography, AppBar, Toolbar, Box, Button } from '@mui/material';
import PredictForm from './components/PredictForm';
import Plot from './components/Plot';
import CarouselComponent from './components/CarouselComponent';
import Contact from './components/Contact';
import { Link as ScrollLink, Element } from 'react-scroll';
import HomeIcon from '@mui/icons-material/Home';
import './App.css';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';

const App = () => {
  const [prediction, setPrediction] = useState(null);
  const [plotSrc, setPlotSrc] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchPlot = (company, date) => {
    setLoading(true);
    const plotUrl = `http://127.0.0.1:5000/plot?company=${company}&date=${date}&${Date.now()}`;
    setPlotSrc(plotUrl);
  };

  return (
    <div className="App">
      <AppBar position="sticky" className="navbar" style={{backgroundColor:"gray"}}>
        <Toolbar>
          <AttachMoneyIcon className="home-icon" />
          <Typography className="Title_main" variant="h4" fontFamily={'"PT Serif"'} padding={'30px'}>
            Predicto
          </Typography>
          <ScrollLink to="form-section" smooth={true} duration={500} className="nav-link">
            <Button color="inherit">Predict Price</Button>
          </ScrollLink>
          <ScrollLink to="contact-section" smooth={true} duration={500} className="nav-link">
            <Button color="inherit">Contact</Button>
          </ScrollLink>
        </Toolbar>
      </AppBar>
      <CarouselComponent />
      <Container maxWidth="lg" className="main-container">
        <Element name="form-section">
          <Grid container spacing={3} className="predict-section">
            <Grid item xs={12} md={4}>
              <PredictForm setPrediction={setPrediction} fetchPlot={fetchPlot} />
              {prediction !== null && (
                <Typography variant="h5" className="prediction" color={'#768aad'}>
                  Predicted stock price on selected date: ${prediction.toFixed(2)}
                </Typography>
              )}
            </Grid>
            <Grid item xs={12} md={8}>
              {loading && (
                <Typography variant="h6" className="loading-message">
                  Your plot is getting ready...
                </Typography>
              )}
              {plotSrc && <Plot src={plotSrc} onLoad={() => setLoading(false)} />}
            </Grid>
          </Grid>
        </Element>
      </Container>
      <Element name="contact-section">
        <Contact />
      </Element>
    </div>
  );
};

export default App;

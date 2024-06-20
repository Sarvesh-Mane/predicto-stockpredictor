import React from 'react';
import { Carousel } from 'react-responsive-carousel';
import 'react-responsive-carousel/lib/styles/carousel.min.css';
import './CarouselComponent.css'; // Custom styles for the carousel
import myImage from './Predict stock prices.jpg';
import myImage2 from './LSTM model for prediction.jpg';
import { Link as ScrollLink } from 'react-scroll';

const CarouselComponent = () => {
  return (
    <Carousel autoPlay infiniteLoop showThumbs={false} verticalSwipe="natural">
      <div className="carousel-slide">
        <img src={myImage} alt="Predict stock prices" />
        <ScrollLink to="form-section" smooth={true} duration={500} className="start-button">
          <button className="get-started-button">Let's get started</button>
        </ScrollLink>
      </div>
      <div className="carousel-slide">
        <img src={myImage2} alt="LSTM Model" />
      </div>
    </Carousel>
  );
};

export default CarouselComponent;

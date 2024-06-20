import React from 'react';
import { Container, Typography, Box } from '@mui/material';

const Contact = () => {
  return (
    <Box className="contact-container" py={5}>
      <Container maxWidth="lg">
        <Typography variant="h4" gutterBottom>
          Contact Us
        </Typography>
        <Typography variant="body1">
          Email: contact@stockpredictionapp.com
        </Typography>
        <Typography variant="body1">
          Phone: +1 234 567 890
        </Typography>
      </Container>
    </Box>
  );
};

export default Contact;

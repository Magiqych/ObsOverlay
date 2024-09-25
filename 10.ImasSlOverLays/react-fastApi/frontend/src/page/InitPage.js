import React, { useEffect, useState } from 'react';
import { Container, Typography, Button } from '@mui/material';
import axios from 'axios';

function InitPage() {
  const [songDetail, setSongDetail] = useState(null);

  useEffect(() => {
    const fetchSongDetail = async () => {
      try {
        const response = await axios.get('/Assets/song_detail.json');
        setSongDetail(response.data);
      } catch (error) {
        console.error('Error fetching song detail:', error);
      }
    };
    fetchSongDetail();
  }, []);

  return (
    <Container>
      <Typography variant="h1" component="h2" gutterBottom>
        Init Page
      </Typography>
      <img src="/Assets/Song.png" alt="Song" />
      {songDetail && (
        <>
          <Typography variant="h5" component="h3" gutterBottom>
            {songDetail.Name}
          </Typography>
          <Typography variant="body1" gutterBottom>
            {songDetail.Description}
          </Typography>
        </>
      )}
      <Button variant="contained" color="primary">
        Click Me
      </Button>
    </Container>
  );
}

export default InitPage;
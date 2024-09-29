import * as React from "react";
import { Card, CardContent, CardMedia, Stack, Typography, Box } from '@mui/material';
// Swiperコンポーネントをインポート
import { Swiper, SwiperSlide } from "swiper/react";
import SwiperCore from "swiper";
import { Autoplay } from "swiper/modules";
import "swiper/swiper-bundle.css";
import { ThemeProvider, createTheme } from '@mui/material/styles'
import * as Icon from '@mui/icons-material';
import './MusicInfo.css';

SwiperCore.use([Autoplay]);

export default function MusicInfo({ songName = "とどけ！アイドル",
  artistName = "作詞：marhy\n作曲・編曲：BNSI（内田哲也）",
  songImage = "/assets/ForTest/Song.png",
  level = "MASTER+",
  levelnum = 25,
  cost = 18,
  notes = 46,
  tapicon = 10,
  longicon = 4,
  flickicon = 4,
  slideicon = 4,
  damageicon = 4,
  dencity = 820,
}) {
  const theme = createTheme({
    palette: {
      mode: 'light',
    }
  })
  // artistNameを改行で分割
  const artistNameLines = artistName.split('\n');
  // levelに基づいてカードの背景色を設定
  const getCardBackgroundColor = (level) => {
    switch (level) {
      case 'DEBUT':
        return 'linear-gradient( 135deg, #90F7EC 10%, #32CCBC 100%);';
      case 'REGULAR':
        return 'linear-gradient( 135deg, #FDEB71 10%, #F8D800 100%);';
      case 'PRO':
        return 'linear-gradient( 135deg, #FEB692 10%, #EA5455 100%);';
      case 'MASTER':
        return "linear-gradient(to top, #fbc2eb 0%, #a6c1ee 100%)";
      case 'MASTER+':
        return 'linear-gradient(45deg, #8c7537 0%, #dbb00b 45%, #fde79d 70%, #dbb10c 85%, #bc7f04 90% 100%);';
      default:
        return theme.palette.background.paper;
    }
  };

  return (
    <ThemeProvider theme={theme}>
    <Card>
      <Box
        sx={{
          position: 'fixed',
          top: 15,
          left: 15,
          background: getCardBackgroundColor(level),
          color: 'white',
          borderRadius: 2,
          padding: 1,
          boxShadow: 3,
        }}
      >
        <Typography variant="body2">
          {level}
        </Typography>
      </Box>
      <Card sx={{ display: 'flex' }}>
        <CardMedia
          component="img"
          sx={{ width: 240, height: 240, objectFit: 'contain' }}
          src={songImage}
          alt="songImage"
        />
        <Box sx={{ display: 'flex', flexDirection: 'column' }}>
          <CardContent sx={{ flex: '1 0 auto' }}>
            <Typography component="div" variant="h5">
              {songName}
            </Typography>
            {artistNameLines.map((line, index) => (
              <Typography
                key={index}
                variant="subtitle1"
                sx={{ color: 'text.secondary' }}
                component="p"
              >
                {line}
              </Typography>
            ))}
          </CardContent>
        </Box>
        <Box sx={{ display: 'flex', flexDirection: 'column' }}>
        </Box>
      </Card>
      
      <Box
        sx={{
          position: 'fixed',
          bottom: 15,
          right: 15,
          backgroundColor: '#455a64',
          color: 'white',
          borderRadius: 2,
          padding: 1,
          boxShadow: 3,
        }}
      >
        <Typography variant="body2">
          THE IDOLM@STER™& ©Bandai Namco Entertainment Inc.
        </Typography>
      </Box>
    </Card>
    </ThemeProvider>
  );
}

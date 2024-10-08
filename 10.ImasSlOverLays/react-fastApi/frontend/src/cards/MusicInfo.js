import * as React from "react";
import { Card, CardContent, CardMedia, Stack, Typography, Box, CardHeader } from '@mui/material';
import Avatar from '@mui/material/Avatar';
import Grid from '@mui/material/Grid2';
import { ThemeProvider, createTheme } from '@mui/material/styles'
// Swiperコンポーネントをインポート
import { Swiper, SwiperSlide } from "swiper/react";
import SwiperCore from "swiper";
import { Autoplay } from "swiper/modules";
import "swiper/swiper-bundle.css";
import './MusicInfo.css';

SwiperCore.use([Autoplay]);

export default function MusicInfo({ data }) {
  const theme = createTheme({
    palette: {
      mode: 'light',
    }
  })
  // JSONデータから曲情報を取得
  const songName = data.Name;
  const artistName = data.Credits;
  const songImage = data.SongImage;
  const selectedLevel = data.SelectedLevel;
  const type = data.Type;
  const length = data.Length;
  const bpm = data.BPM;
  const releaseDate = data.ReleaseDate;
  const levelnum = data.Level;
  const cost = data.Cost;
  const notes = data.Notes;
  const tapicon = data.TapIcon;
  const longicon = data.LongIcon;
  const flickicon = data.FlickIcon;
  const slideicon = data.SlideIcon;
  const damegeicon = data.DamageIcon;
  const dencity = data.Dencity;

  // artistNameを改行で分割
  const artistNameLines = artistName.split('\n');
  // levelに基づいてカードの背景色を設定
  const getCardBackgroundColor = (selectedLevel) => {
    switch (selectedLevel) {
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
  // Typeに基づいてカードのアイコンを選択
  const getTypeIcon = (type) => {
    switch (type) {
      case '全タイプ':
        return './assets/icon/all.webp';
      case 'クール':
        return '/assets/icon/cool.webp';
      case 'キュート':
        return '/assets/icon/cute.webp';
      case 'パッション':
        return '/assets/icon/passion.webp';
      default:
        return './assets/icon/all.webp';
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <div
        style={{
          position: "absolute",
          left: "360px",
          bottom: 0,
          height: "280px",
          width: "1300px",
        }}
      >{/* レベル表示 */}
      <Box
        sx={{
          position: 'relative',
          top: 20,
          left: -10,
          background: getCardBackgroundColor(selectedLevel),
          color: 'white',
          borderRadius: 2,
          padding: 1,
          boxShadow: 3,
          height: 20,
          width: 100,
          zIndex: 1,
        }}
      >
        <Typography variant="body2">
          {selectedLevel}
        </Typography>
      </Box>
        <Card sx={{ display: 'flex' }}>
          {/*楽曲画像表示*/}
          <CardMedia
            component="img"
            sx={{ width: 240, height: 240, objectFit: 'contain'}}
            src={songImage}
            alt="songImage"
          />
          <Grid container spacing={1} sx={{ width: '100%', margin: 1, flexDirection: 'column' }}>
            <card>
              <CardHeader
                avatar={
                  <Avatar src={getTypeIcon(type)} aria-label="avater" />
                }
                title={<Typography variant="h5" component="div" sx={{ width: '100%', 'margin-left': 1 }}>
                  {songName}
                </Typography>}
              />
            </card>
            <Grid sx={{ flexGrow: 1, display: 'flex' }}>
              <card >
                <CardHeader
                  avatar={
                    <Avatar src='/assets/icon/composing.png' aria-label="avater" />
                  }
                  title="Credit"
                  subheader={artistNameLines.map((line, index) => (
                    <Typography key={index} variant="body2">
                      {line}
                    </Typography>
                  ))}
                />
              </card>
              <Grid sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
                <Grid sx={{ flexGrow: 1, display: 'flex' }}>
                  <card >
                    <CardHeader
                      avatar={
                        <Avatar src='/assets/icon/new-release.png' aria-label="avater" />
                      }
                      title="Release"
                      subheader={releaseDate}
                    />
                  </card>
                  <card >
                    <CardHeader
                      avatar={
                        <Avatar src='/assets/icon/LengthIcon.png' aria-label="avater" />
                      }
                      title="Length"
                      subheader={length}
                    />
                  </card>
                  <card >
                    <CardHeader
                      avatar={
                        <Avatar src='/assets/icon/metronome.png' aria-label="avater" />
                      }
                      title="BPM"
                      subheader={bpm}
                    />
                  </card>
                  <card >
                    <CardHeader
                      avatar={
                        <Avatar src='/assets/icon/rank-badge.png' aria-label="avater" />
                      }
                      title="Level"
                      subheader={levelnum}
                    />
                  </card>
                  <card >
                    <CardHeader
                      avatar={
                        <Avatar src='/assets/icon/sun-energy.png' aria-label="avater" />
                      }
                      title="Stamina"
                      subheader={cost}
                    />
                  </card>
                </Grid>
                <Grid sx={{ flexGrow: 1, display: 'flex' }}>
                  <card >
                    <CardHeader
                      avatar={
                        <Avatar src='/assets/icon/musical-note.png' aria-label="avater" />
                      }
                      title="Notes"
                      subheader={notes}
                    />
                  </card>
                  <card >
                    <CardHeader
                      avatar={
                        <Avatar src='/assets/icon/touch.png' aria-label="avater" />
                      }
                      title="Tap"
                      subheader={tapicon}
                    />
                  </card>
                  <card >
                    <CardHeader
                      avatar={
                        <Avatar src='/assets/icon/hold.png' aria-label="avater" />
                      }
                      title="Long"
                      subheader={longicon}
                    />
                  </card>
                  <card >
                    <CardHeader
                      avatar={
                        <Avatar src='/assets/icon/flick.png' aria-label="avater" />
                      }
                      title="Flick"
                      subheader={flickicon}
                    />
                  </card>
                  <card >
                    <CardHeader
                      avatar={
                        <Avatar src='/assets/icon/scrolling.png' aria-label="avater" />
                      }
                      title="Slide"
                      subheader={slideicon}
                    />
                  </card>
                </Grid>
              </Grid>
            </Grid>
          </Grid>
        </Card>
      </div>
    </ThemeProvider>
  );
}

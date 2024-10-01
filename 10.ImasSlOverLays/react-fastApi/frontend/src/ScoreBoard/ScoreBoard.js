import * as React from "react";
import { Card, CardContent, CardMedia, Stack, Typography, Box, CardHeader } from '@mui/material';
import Avatar from '@mui/material/Avatar';
import Grid from '@mui/material/Grid2';
import { ThemeProvider, createTheme } from '@mui/material/styles'
import MyPolar from "./MyPolar";
import MyBar from "./MyBar";
export default function ScoreBoard({ SongData, ScoreData }) {
  const theme = createTheme({
    palette: {
      mode: 'light',
    }
  })
  //Pageレイアウト変数
  const pagewidth = 1300;
  const pageheight = 1000;
  // JSONデータから曲情報を取得
  const songname = SongData.Name;
  const songimage = SongData.SongImage;
  const selectedlevel = SongData.SelectedLevel;
  // JSONデータからスコア情報を取得
  const perfect = ScoreData.PERFECT;
  const great = ScoreData.GREAT;
  const nice = ScoreData.NICE;
  const bad = ScoreData.BAD;
  const miss = ScoreData.MISS;
  const combo = ScoreData.COMBO;
  const score = ScoreData.SCORE;
  const highscore = ScoreData.HIGHSCORE;
  const urpm = ScoreData.URPM;
  const rpm = ScoreData.RPM;



  // チャートデータ
  const dataforpolar = {
    labels: [ "PERFECT","GREAT", "NICE", "BAD", "MISS"],
    datasets: [
      {
        data: [ perfect,great, nice, bad, miss]
      },
    ],
  };


  return (
    <ThemeProvider theme={theme}>
      <Grid container spacing={2} sx={{ width: pageheight, height: pageheight, display: 'flex', flexDirection: 'column' }}>
        <Grid container spacing={2} sx={{ width: pageheight,height: 70, display: 'flex' }}>
          <Grid>
            <Card sx={{ width: 300 }}>
              <CardContent>
                <Typography variant="h6">
                  Result
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid sx={{ flexGrow: 1 }}>
            <Card sx={{ display: 'flex' }}>
              {/*楽曲画像表示*/}
              <CardMedia
                component="img"
                sx={{ width: 70, height: 70, objectFit: 'contain' }}
                src={songimage}
                alt="songimage"
              />
              <Grid sx={{ display: 'flex', 'margin-left': '10px', flexDirection: 'column' }}>
                <Typography variant="h6">
                  {songname}
                </Typography>
                <Typography variant="h6">
                  {selectedlevel}
                </Typography>
              </Grid>
            </Card>
          </Grid>
        </Grid>
        <Grid sx={{ width: '100%', height: 300, flexDirection: 'column' }}>
          <Card sx={{ width: 600 ,height :100}}>
            <MyBar data={dataforpolar} />
          </Card>

        </Grid>

      </Grid>
    </ThemeProvider>
  );
}
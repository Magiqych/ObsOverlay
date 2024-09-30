import * as React from "react";
import { Card, CardContent, CardMedia, Stack, Typography, Box, CardHeader } from '@mui/material';
import Avatar from '@mui/material/Avatar';
import Grid from '@mui/material/Grid2';
import { MusicInfo } from "../cards";
import MyResponsivePie from "./MyResponsivePie";
import { ThemeProvider, createTheme } from '@mui/material/styles'

export default function ScoreBoard({ SongData ,ScoreData}) {
  const theme = createTheme({
    palette: {
      mode: 'light',
    }
  })
  return (
    <ThemeProvider theme={theme}>
    <Card sx={{width:1000,height:600}}>
      <grid container spacing={2} sx={{width:500,height:600}}>
        <MusicInfo data={SongData}/>
        <MyResponsivePie data={ScoreData}/>
      </grid>
    </Card>
    </ThemeProvider>
  );
}
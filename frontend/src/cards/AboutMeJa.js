import * as React from 'react';
import { styled } from '@mui/material/styles';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardMedia from '@mui/material/CardMedia';
import CardContent from '@mui/material/CardContent';
import Avatar from '@mui/material/Avatar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import { red } from '@mui/material/colors';
import Stack from "@mui/material/Stack";

const ExpandMore = styled((props) => {
  const { expand, ...other } = props;
  return <IconButton {...other} />;
})(({ theme }) => ({
  marginLeft: 'auto',
  transition: theme.transitions.create('transform', {
    duration: theme.transitions.duration.shortest,
  }),
  variants: [
    {
      props: ({ expand }) => !expand,
      style: {
        transform: 'rotate(0deg)',
      },
    },
    {
      props: ({ expand }) => !!expand,
      style: {
        transform: 'rotate(180deg)',
      },
    },
  ],
}));

export default function AboutMeJa() {
  return (
    <Card>
      <Stack direction="hori" spacing={2}>
        <CardHeader
          avatar={
            <Avatar alt="Youtube" src="assets/Magiqych/Magiqych.jpg" />
          }
          title="Youtube"
          subheader="youtube.com/@magiqy_ch"
        />
        <CardHeader
          avatar={
            <Avatar alt="Github" src="assets/static/GameLogo.webp" />
          }
          title="デレステ"
          subheader="GameID:827459216"
        />
      </Stack>
      <CardContent>
      <Typography
          variant="h6"
          component="h2"
          sx={{ color: "text.secondary" }}
        >
ゲーム、漫画、アニメから釣り私の趣味や生活をシェアしています。<br />
YouTubeを通じて世界中の人々とつながりたいと思っています。<br />
このチャンネルには特定の目標はありません。目標がないことが目標です。人生は予測不可能で、このチャンネルも同様です。祇園精舎の鐘の声、諸行無常の響きあり。それが私の人生のテーマです。
        </Typography>
      </CardContent>
    </Card>
  );
}
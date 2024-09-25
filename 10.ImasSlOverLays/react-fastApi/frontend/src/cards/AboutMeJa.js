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
      <CardHeader
        avatar={
            <Avatar alt="Remy Sharp" src="Assets/Magiqych/Magiqych.jpg" />
        }
        title="このチャンネルについて"
        subheader="@magiqy_ch"
      />
      <CardContent>
        <Typography variant="body2" sx={{ color: 'text.secondary' }}>
ここでは、ゲーム、漫画、アニメから釣りやその他のサブカルチャーまで、私の趣味や生活をシェアしています。
特定のターゲット視聴者はいませんが、YouTubeを通じて世界中の人々とつながりたいと思っています。
私の動画は無編集でありのままの姿を見せるもので、世界に「俺はここにいるんだ」と伝えるためのものです。
このチャンネルには特定の目標はありません。目標がないことが目標です。人生は予測不可能で、このチャンネルも同様です。
祇園精舎の鐘の声、諸行無常の響きあり。それが私の人生のテーマです。
        </Typography>
      </CardContent>
    </Card>
  );
}
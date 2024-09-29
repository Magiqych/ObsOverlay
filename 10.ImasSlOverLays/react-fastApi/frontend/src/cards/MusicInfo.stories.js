import React from 'react';
import MusicInfo from './MusicInfo';

export default {
  title: 'Cards/MusicInfo',
  component: MusicInfo,
};

const Template = (args) => <MusicInfo {...args} />;
export const Default = Template.bind({});
Default.args = {
  songName:"とどけ！アイドル",
  artistName:"作詞：marhy\n作曲・編曲：BNSI（内田哲也）",
  songImage:"/assets/ForTest/Song.png",
  level:"MASTER+",
  levelnum:25,
  cost:18,
  notes:46,
  tapicon:10,
  longicon:4,
  flickicon:4,
  slideicon:4,
  damageicon:4,
  dencity:820
};
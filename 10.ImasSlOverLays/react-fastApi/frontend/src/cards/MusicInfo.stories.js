import React from 'react';
import MusicInfo from './MusicInfo';
import songDetail from '../assets/test/song_detail.json';
// テストデータをインポート
export default {
  title: 'Cards/MusicInfo',
  component: MusicInfo,
};
const Template = (args) => <MusicInfo {...args} />;
export const Default = Template.bind({});
Default.args = {
  data : songDetail,
};
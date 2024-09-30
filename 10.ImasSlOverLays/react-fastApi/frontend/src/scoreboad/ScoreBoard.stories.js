import React from 'react';
import ScoreBoard from './ScoreBoard';
// テストデータをインポート
import songDetail from '../assets/test/song_detail.json';
import scoreData from '../assets/test/ScoreTest.json';


export default {
  title: 'scoreboad/ScoreBoard',
  component: ScoreBoard,
};

const Template = (args) => <ScoreBoard {...args} />;
export const Default = Template.bind({});
Default.args = {
  SongData : songDetail,
  ScoreData:scoreData
};
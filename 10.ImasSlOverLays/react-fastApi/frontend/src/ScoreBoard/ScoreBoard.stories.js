import React from 'react';
import ScoreBoard from './ScoreBoard'; // インポート文を修正
// テストデータをインポート
import songDetail from '../assets/test/song_detail.json';
import scoreData from '../assets/test/ScoreTest.json';
import records from '../assets/test/records.json';

export default {
  title: 'ScoreBoard/ScoreBoard',
  component: ScoreBoard,
};

const Template = (args) => <ScoreBoard {...args} />;
export const Default = Template.bind({});
Default.args = {
  SongData: songDetail,
  ScoreData: scoreData,
  RecordsData:records
};
import React from 'react';
import ScoreBoard from './ScoreBoard'; // インポート文を修正
// テストデータをインポート
import songDetail from '../assets/test/song_detail.json';
import scoreData from '../assets/test/ScoreTest.json';
import records from '../assets/test/records.json';
import fewrecords from '../assets/test/fewrecords.json';
import somerecords from '../assets/test/somerecords.json';

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
export const NoRecord = Template.bind({});
NoRecord.args = {
  SongData: songDetail,
  ScoreData: scoreData,
  RecordsData:[]
};
export const FewRecord = Template.bind({});
FewRecord.args = {
  SongData: songDetail,
  ScoreData: scoreData,
  RecordsData:fewrecords
};
export const SomeRecord = Template.bind({});
SomeRecord.args = {
  SongData: songDetail,
  ScoreData: scoreData,
  RecordsData:somerecords
};
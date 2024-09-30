import React from 'react';
import MyResponsivePie from './MyResponsivePie';
// テストデータをインポート
import scoreData from '../assets/test/ScoreTest.json';


export default {
  title: 'MyResponsivePie/MyResponsivePie',
  component: MyResponsivePie,
};

const Template = (args) => <MyResponsivePie {...args} />;
export const Default = Template.bind({});
Default.args = {
  ScoreData:scoreData
};
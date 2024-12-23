import React from 'react';
import MyBar from './MyBar';

export default {
  title: 'ScoreBoard/MyBar',
  component: MyBar,
};

const Template = (args) => <MyBar {...args} />;

export const Default = Template.bind({});
Default.args = {};
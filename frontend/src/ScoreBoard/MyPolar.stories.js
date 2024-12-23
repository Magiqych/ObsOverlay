import React from 'react';
import MyPolar from './MyPolar';

export default {
  title: 'ScoreBoard/MyPolar',
  component: MyPolar,
};

const Template = (args) => <MyPolar {...args} />;

export const Default = Template.bind({});
Default.args = {};
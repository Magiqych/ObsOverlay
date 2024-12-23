import React from 'react';
import MyResponsiveLine from './MyResponsiveLine';

export default {
  title: 'ScoreBoard/MyResponsiveLine',
  component: MyResponsiveLine,
};

const Template = (args) => <MyResponsiveLine {...args} />;

export const Default = Template.bind({});
Default.args = {};
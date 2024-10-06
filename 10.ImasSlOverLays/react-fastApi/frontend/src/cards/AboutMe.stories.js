import React from 'react';
import AboutMe from './AboutMe';

export default {
  title: 'Cards/AboutMe',
  component: AboutMe,
};

const Template = (args) => <AboutMe {...args} />;

export const Default = Template.bind({});
Default.args = {};
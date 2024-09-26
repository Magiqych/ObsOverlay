import React from 'react';
import AboutImas from './AboutImas';

export default {
  title: 'Cards/AboutImas',
  component: AboutImas,
};

const Template = (args) => <AboutImas {...args} />;

export const Default = Template.bind({});
Default.args = {};
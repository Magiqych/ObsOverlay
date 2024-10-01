import React from 'react';
import { PolarArea } from 'react-chartjs-2';
import { Chart, CategoryScale,RadialLinearScale, ArcElement, Tooltip, Legend } from 'chart.js';
// Chart.jsのスケールとチャートタイプを登録
Chart.register(CategoryScale,RadialLinearScale, ArcElement, Tooltip, Legend);

const defaultdata = {
  labels: ["Physical", "Mental", "Practical", "Spiritual", "Social", "Work"],
  datasets: [
    {
      data: [1.7, 3.7, 2, 4, 2.2, 4.5],
      backgroundColor: [
        "#B14FC5",
        "#9CCA2B",
        "#54C8E8",
        "#EE6FBB",
        "#FFD100",
        "#FF7F30"
      ]
    }
  ]
};

export default function MyPolar({ data = defaultdata }) {
  return (
    <div>
      <PolarArea data={data} />
    </div>
  );
}
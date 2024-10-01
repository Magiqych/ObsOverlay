import React from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart, CategoryScale, LogarithmicScale,LinearScale, BarElement, Title, Tooltip, Legend, Ticks } from 'chart.js';

// Chart.jsのスケールとチャートタイプを登録
Chart.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend,LogarithmicScale);

const defaultdata = {
  labels: [ "PERFECT","GREAT", "NICE", "BAD", "MISS"],
  datasets: [
    {
      label:"rawdata",
      data: [ 514,14, 6,2,5],
      backgroundColor: [
        "#9CCA2B",
        "#54C8E8",
        "#EE6FBB",
        "#FFD100",
        "#FF7F30"
      ]
    },
  ],
};


const options = {
  indexAxis: 'y', // 横向きの積み上げグラフにする
  scales: {
    x: {
      type: 'logarithmic',
      beginAtZero: true
    }
  },
  plugins: {
    legend: {
      position: 'top'
    },
    title: {
      display: true,
      text: 'スコア'
    },
  }
};

// const options = {
//   scales: {
//     y: {
//       type: 'logarithmic',
//       beginAtZero: true,
//       ticks: {
//         callback: function(value, index, values) {
//           return Number(value.toString()); // 10の累乗を表示
//         }
//       }
//     }
//   }
// };

export default function MyBar({ data = defaultdata }) {
  return (
    <div>
      <Bar data={data} options={options} />
    </div>
  );
}
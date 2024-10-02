import React from 'react';
import { ResponsiveLine } from '@nivo/line'
import { height, maxHeight, maxWidth, width } from '@mui/system';
const MyResponsiveLine = ({ data }) => {
    return (
        <ResponsiveLine
            areaOpacity={0.07}
            colors={[
                'rgb(97, 205, 187)',
                'rgb(244, 117, 96)'
            ]}
            crosshairType="cross"
            curve="monotoneX"
            data={[
                {
                    data: [
                        {
                            x: 0,
                            y: 0.7
                        },
                        {
                            x: 1,
                            y: 0.9
                        },
                        {
                            x: 2,
                            y: 0.8
                        },
                        {
                            x: 3,
                            y: 0.6
                        },
                        {
                            x: 4,
                            y: 0.3
                        },
                        {
                            x: 5,
                            y: 0
                        },
                        {
                            x: 6,
                            y: null
                        },
                        {
                            x: 7,
                            y: null
                        },
                        {
                            x: 8,
                            y: null
                        },
                        {
                            x: 9,
                            y: null
                        },
                        {
                            x: 10,
                            y: null
                        },
                        {
                            x: 11,
                            y: 0
                        },
                        {
                            x: 12,
                            y: 0.4
                        },
                        {
                            x: 13,
                            y: 0.6
                        },
                        {
                            x: 14,
                            y: 0.5
                        },
                        {
                            x: 15,
                            y: 0.3
                        },
                        {
                            x: 16,
                            y: 0.4
                        },
                        {
                            x: 17,
                            y: 0
                        }
                    ],
                    id: 'positive :)'
                },
                {
                    data: [
                        {
                            x: 5,
                            y: 0
                        },
                        {
                            x: 6,
                            y: -0.3
                        },
                        {
                            x: 7,
                            y: -0.5
                        },
                        {
                            x: 8,
                            y: -0.9
                        },
                        {
                            x: 9,
                            y: -0.2
                        },
                        {
                            x: 10,
                            y: -0.4
                        },
                        {
                            x: 11,
                            y: 0
                        },
                        {
                            x: 12,
                            y: null
                        },
                        {
                            x: 13,
                            y: null
                        },
                        {
                            x: 14,
                            y: null
                        },
                        {
                            x: 15,
                            y: null
                        },
                        {
                            x: 16,
                            y: null
                        },
                        {
                            x: 17,
                            y: 0
                        },
                        {
                            x: 18,
                            y: -0.4
                        },
                        {
                            x: 19,
                            y: -0.2
                        },
                        {
                            x: 20,
                            y: -0.1
                        },
                        {
                            x: 21,
                            y: -0.6
                        }
                    ],
                    id: 'negative :('
                }
            ]}
            enableArea
            xScale={{
                max: 'auto',
                min: 'auto',
                type: 'linear'
            }}
            yScale={{
                max: 'auto',
                min: 'auto',
                type: 'linear'
            }}
            enableGridX={false}
            axisTop={null}
            axisRight={null}
            axisLeft={null}
            axisBottom={null}
            pointSize={0}
            theme={{
                grid: {
                    line: {
                        strokeWidth: 0,
                    },
                }
            }}
        />
)
}
export default MyResponsiveLine;
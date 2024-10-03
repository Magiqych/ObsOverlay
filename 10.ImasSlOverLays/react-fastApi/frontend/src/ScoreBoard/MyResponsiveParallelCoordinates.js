import React, { useState, useEffect } from 'react';
import { ResponsiveParallelCoordinates } from '@nivo/parallel-coordinates'
import generateParallelCoordinatesData from './generateParallelCoordinatesData'; // 関数のインポート

const MyResponsiveParallelCoordinates = ({ scoreInfo, recordInfo,members,limit}) => {
    const [data, setData] = useState([]);
    const [variables, setVariables] = useState([]);
    useEffect(() => {
        const reversedMembers = [...members].reverse(); // members 配列を逆順にする
        const { data, variables } = generateParallelCoordinatesData(scoreInfo, recordInfo, reversedMembers,limit);
        setData(data);
        setVariables(variables);
    }, [scoreInfo, recordInfo, members,limit]);
    return(
    <ResponsiveParallelCoordinates
        data={data}
        variables={variables}
        margin={{ top: 50, right: 200, bottom: 50, left: 60 }}
        layout="vertical"
        lineWidth={3}
        legends={[
            {
                anchor: 'right',
                direction: 'column',
                justify: false,
                translateX: 100,
                translateY: 0,
                itemsSpacing: 2,
                itemWidth: 60,
                itemHeight: 20,
                itemDirection: 'left-to-right',
                itemOpacity: 0.85,
                symbolSize: 20,
                effects: [
                    {
                        on: 'hover',
                        style: {
                            itemOpacity: 1
                        }
                    }
                ]
            }
        ]}
    />
    )
    };
export default MyResponsiveParallelCoordinates;
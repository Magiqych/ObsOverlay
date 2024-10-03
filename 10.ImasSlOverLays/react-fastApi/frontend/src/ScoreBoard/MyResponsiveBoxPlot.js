import React from 'react';
import { ResponsiveBoxPlot } from '@nivo/boxplot';

// ボックスプロットコンポーネント
const MyResponsiveBoxPlot = ({ data }) => {
    return (
        <ResponsiveBoxPlot
            data={data}
            margin={{ top: 40, right: 40, bottom: 40, left: 40 }}
            padding={0.3}
            groupMode="grouped"
            yScale={{
                type: 'symlog'
            }}
            colors={['#ffaacf', '#ffcc79', '#a0d9ff', '#aede70']}
            colorBy='group'
            theme={{
                axis: {
                    ticks: {
                        text: {
                            fontSize: 11,
                            fill: '#ffffff',
                            outlineWidth: 0,
                            outlineColor: 'transparent'
                        }
                    }
                }
            }}
        />
    )
}

export default MyResponsiveBoxPlot;
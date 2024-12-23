import React from 'react';
import { ResponsiveLine } from '@nivo/line'
import { height, maxHeight, maxWidth, width } from '@mui/system';
const MyResponsiveLine = ({ data }) => {
    return (
        <ResponsiveLine
            areaOpacity={0.07}
            colors={[
                'rgb(255,255,255)'
            ]}
            crosshairType="cross"
            data={data}
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
            useMesh={true}
            enableSlices="x"
            curve="monotoneX" // 補完オプションを設定
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
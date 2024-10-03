import React from 'react';
import { height, maxHeight, maxWidth, width } from '@mui/system';
import { ResponsiveRadialBar } from '@nivo/radial-bar'

const MyResponsiveRadialBar = ({ data }) => {
        // カスタムテーマを定義
        const customTheme = {
            axis: {
                ticks: {
                    line: {
                        stroke: "#777777",
                        strokeWidth: 1
                    },
                    text: {
                        fontSize: 11,
                        fill: "#ffffff", // グリッドのテキスト色を白に設定
                        outlineWidth: 0,
                        outlineColor: "transparent"
                    }
                }
            }
        };

    return (
        <ResponsiveRadialBar
            data={data}
            valueFormat=">-.2f"
            padding={0.4}
            cornerRadius={2}
            margin={{ top: 30, right: 20, bottom: 30, left: 20 }}
            circularAxisOuter={{ tickSize: 5, tickPadding: 12, tickRotation: 0 }}
            // カスタムカラー関数を指定
            colors={['#48d1cc','#4481eb','#ba55d3']}
            
            radialAxisStart={{
                tickSize: 5,
                tickPadding: 5,
                tickRotation: 0,
                tickTextColor: '#ffffff' // グリッドのテキスト色を白に設定
            }}
            theme={customTheme} // カスタムテーマを指定
            motionConfig="slow"
            legends={[]}
        />
    )
}
export default MyResponsiveRadialBar;
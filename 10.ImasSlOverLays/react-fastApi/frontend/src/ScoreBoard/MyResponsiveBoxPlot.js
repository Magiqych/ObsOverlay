import React from 'react';
import { ResponsiveBoxPlot } from '@nivo/boxplot';
import generateBoxPlotData from './generateBoxPlotData'; // ボックスプロットデータ生成関数をインポート

// ボックスプロットコンポーネント
const MyResponsiveBoxPlot = ({ recordInfo, members }) => {
    let boxPlotData = [];
    try {
        if (!recordInfo || Object.keys(recordInfo).length === 0) {
            throw new Error("recordInfo is empty or not set");
        }
        boxPlotData = generateBoxPlotData(recordInfo, members);
    } catch (error) {
        console.error("Error generating box plot data:", error.message);
        // 必要に応じて、デフォルト値を設定するか、他のエラーハンドリングを行います
        boxPlotData = []; // 例として空の配列を設定
    }
    if (boxPlotData.length < 10) {
        return (
            <div style={{display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
                <p style={{ color: 'white', margin: 0 }}>
                    Data is too sparse to display the box plot
                </p>
            </div>
        )
    }
    else {
        return (
            <ResponsiveBoxPlot
                data={boxPlotData}
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
}

export default MyResponsiveBoxPlot;
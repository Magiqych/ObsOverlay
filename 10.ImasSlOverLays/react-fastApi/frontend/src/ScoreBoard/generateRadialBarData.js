const generateRadialBarData = (scoreInfo, recordInfo, recordNum) => {
    if (!scoreInfo || !recordInfo) {
        console.error('Invalid scoreInfo or recordInfo:', scoreInfo, recordInfo); // デバッグ用
        return [];
    }

    const highScoreData = {
        id: 'HighScore',
        data: [
            { x: 'HIGHSCORE', y: scoreInfo.HIGHSCORE.value }
        ]
    };

    const scoreData = {
        id: 'Score',
        data: [
            { x: 'ScoreNOW', y: scoreInfo.SCORE.value }
        ]
    };
    // recordInfoのScoreプロパティに保持されているスコアの履歴データを利用してソートし、recordNum個取得
    const sortedData = recordInfo.SCORE
        .map((SCORE, index) => ({
            SCORE,
            date: recordInfo.DATE[index]
        }))
        .sort((a, b) => b - a)
        .slice(0, recordNum);
    const fieldData = sortedData.map((item, index) => ({
        id: `Score@${item.date}`,
        data: [
            {
                x: 'ScorePast',
                y: item.SCORE
            }
        ]
    }));
    const data = [ ...fieldData, scoreData,highScoreData];
    return data;
};

export default generateRadialBarData;
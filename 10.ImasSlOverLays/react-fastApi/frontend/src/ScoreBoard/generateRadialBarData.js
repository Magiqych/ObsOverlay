const generateRadialBarData = (scoreInfo) => {
    if (!scoreInfo) {
        console.error('Invalid scoreInfo or recordInfo:', scoreInfo); // デバッグ用
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
    const data = [scoreData,highScoreData];
    return data;
};

export default generateRadialBarData;
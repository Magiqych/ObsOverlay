const generateParallelCoordinatesData = (scoreInfo, recordInfo, members, limit) => {
    // データを作成
    const data = [];
    // variablesを作成
    const variables = members.map(member => ({
        id: member,
        label: member,
        value: member,
        min: 'auto',
        max: 'auto',
        ticksPosition: 'before',
        legendPosition: 'start',
        legendOffset: 20
    }));
    // スコア情報を追加
    const scoreData = {};
    members.forEach(member => {
        scoreData[member] = scoreInfo[member].value;
    });
    scoreData.id = "NOW"; // ID設定
    data.push(scoreData);
    // recordInfoがない場合は処理をスキップ
    if (!recordInfo || Object.keys(recordInfo).length === 0) {
        return { data, variables };
    }
    // レコード情報を追加
    const recordCount = Math.min(recordInfo[members[0]].length, limit); // 各メンバーの配列の長さと上限を比較
    for (let i = 0; i < recordCount; i++) {
        const recordData = {};
        members.forEach(member => {
            recordData[member] = recordInfo[member][i];
        });
        recordData.id = recordInfo.DATE[i]; // 各レコードのIDを日付に設定
        data.push(recordData);
    }
    return { data, variables };
};

export default generateParallelCoordinatesData;
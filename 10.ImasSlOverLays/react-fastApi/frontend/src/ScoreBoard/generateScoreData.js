const generateScoreData = (recordInfo, field, dataCount) => {
  if (!recordInfo) {
    console.error('Invalid recordInfo:', recordInfo); // デバッグ用
    return [];
  }

  if (!recordInfo[field]) {
    console.error(`Invalid field: ${field}`, recordInfo); // デバッグ用
    return [];
  }

  const limitedData = recordInfo.DATE.slice(0, dataCount).map((date, index) => ({
    x: new Date(date).getTime(), // Dateをタイムスタンプに変換
    y: recordInfo[field][index]
  }));

  const data = [
    {
      id: field,
      data: limitedData
    }
  ];

  console.log('Generated Data:', data); // デバッグ用
  return data;
};

export default generateScoreData;
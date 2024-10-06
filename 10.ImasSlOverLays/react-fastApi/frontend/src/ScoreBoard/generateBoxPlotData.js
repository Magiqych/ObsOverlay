const calculateMean = (values) => {
    const sum = values.reduce((acc, val) => acc + val, 0);
    return sum / values.length;
};

const calculateMedian = (values) => {
    const sortedValues = values.slice().sort((a, b) => a - b);
    const middleIndex = Math.floor(sortedValues.length / 2);

    if (sortedValues.length % 2 === 0) {
        return (sortedValues[middleIndex - 1] + sortedValues[middleIndex]) / 2;
    } else {
        return sortedValues[middleIndex];
    }
};

const calculateStandardDeviation = (values, mean) => {
    const variance = values.reduce((acc, val) => acc + Math.pow(val - mean, 2), 0) / values.length;
    return Math.sqrt(variance);
};

const generateBoxPlotData = (recordInfo, members) => {
    const data = members.flatMap(member => {
        if (!recordInfo[member]) {
            console.error('Invalid member:', member); // デバッグ用
            return [];
        }

        const values = recordInfo[member];
        const mean = calculateMean(values);
        const median = calculateMedian(values);
        const sd = calculateStandardDeviation(values, mean);
        const n = values.length;

        return values.map(value => ({
            group: member,
            mu: median,
            sd: sd,
            n: n,
            value: value
        }));
    });
    return data;
};

export default generateBoxPlotData;
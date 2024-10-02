// レコード情報クラス
class RecordInfo {
  // レコード情報を格納する配列
  constructor(records) {
    this.PERFECT = records.map(record => record.Perfect);
    this.GREAT = records.map(record => record.Great);
    this.NICE = records.map(record => record.Nice);
    this.BAD = records.map(record => record.Bad);
    this.MISS = records.map(record => record.Miss);
    this.COMBO = records.map(record => record.Combo);
    this.SCORE = records.map(record => record.Score);
    this.HIGHSCORE = records.map(record => record.HighScore);
    this.PRP = records.map(record => record.Prp);
    this.UPRP = records.map(record => record.UPrp);
    this.DATE = records.map(record => record.Date);
    this.AVERAGEPERFECT = this.calculateAverage(this.PERFECT);
    this.AVERAGEGREAT = this.calculateAverage(this.GREAT);
    this.AVERAGENICE = this.calculateAverage(this.NICE);
    this.AVERAGEBAD = this.calculateAverage(this.BAD);
    this.AVERAGEMISS = this.calculateAverage(this.MISS);
    this.AVERAGECOMBO = this.calculateAverage(this.COMBO);
    this.AVERAGESCORE = this.calculateAverage(this.SCORE);
    this.AVERAGEHIGHSCORE = this.calculateAverage(this.HIGHSCORE);
  }

  calculateAverage(values) {
    const validValues = values.filter(value => value !== undefined && value !== null);
    const sum = validValues.reduce((acc, value) => acc + value, 0);
    return validValues.length ? sum / validValues.length : 0;
  }
}

export default RecordInfo;
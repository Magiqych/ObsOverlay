const allowupsrc = '/assets/icon/arrowUp.png';
const allowdownsrc = '/assets/icon/arrowDown.png';
const alowflatsrc = '/assets/icon/arrowFlat.png';

class ScoreInfo {
  constructor(ScoreData, latestRecord) {
    this.allnotes = ScoreData.PERFECT + ScoreData.GREAT + ScoreData.NICE + ScoreData.BAD + ScoreData.MISS;
    this.ScoreData = ScoreData;
    this.latestRecord = latestRecord;
    this.info = this.calculateScoreInfo();
  }

  calculateScoreInfo() {
    if (!this.latestRecord) {
      return this.createInitialScoreInfo();
    } else {
      return this.createUpdatedScoreInfo();
    }
  }

  createInitialScoreInfo() {
    return {
      PERFECT: this.createScoreDetail(this.ScoreData.PERFECT, 0, alowflatsrc),
      GREAT: this.createScoreDetail(this.ScoreData.GREAT, 0, alowflatsrc),
      NICE: this.createScoreDetail(this.ScoreData.NICE, 0, alowflatsrc),
      BAD: this.createScoreDetail(this.ScoreData.BAD, 0, alowflatsrc),
      MISS: this.createScoreDetail(this.ScoreData.MISS, 0, alowflatsrc),
      COMBO: this.createScoreDetail(this.ScoreData.COMBO, 0, alowflatsrc, false),
      SCORE: this.createScoreDetail(this.ScoreData.SCORE, 0, alowflatsrc, false),
      HIGHSCORE: this.createScoreDetail(this.ScoreData.HIGHSCORE, 0, alowflatsrc, false),
      URPM: this.createScoreDetail(this.ScoreData.URPM, 0, alowflatsrc, false),
      RPM: this.createScoreDetail(this.ScoreData.RPM, 0, alowflatsrc, false),
      allnotes: this.allnotes
    };
  }

  createUpdatedScoreInfo() {
    const difperfect = this.ScoreData.PERFECT - this.latestRecord.Perfect;
    const difgreat = this.ScoreData.GREAT - this.latestRecord.Great;
    const difnice = this.ScoreData.NICE - this.latestRecord.Nice;
    const difbad = this.ScoreData.BAD - this.latestRecord.Bad;
    const difmiss = this.ScoreData.MISS - this.latestRecord.Miss;
    const difcombo = this.ScoreData.COMBO - this.latestRecord.Combo;
    const difscore = this.ScoreData.SCORE - this.latestRecord.Score;
    const difhighscore = this.ScoreData.HIGHSCORE - this.latestRecord.HighScore;
    const difurpm = this.ScoreData.URPM - this.latestRecord.URPM;
    const difrpm = this.ScoreData.RPM - this.latestRecord.RPM;

    return {
      PERFECT: this.createScoreDetail(this.ScoreData.PERFECT, difperfect, this.getIcon(difperfect)),
      GREAT: this.createScoreDetail(this.ScoreData.GREAT, difgreat, this.getIcon(difgreat)),
      NICE: this.createScoreDetail(this.ScoreData.NICE, difnice, this.getIcon(difnice)),
      BAD: this.createScoreDetail(this.ScoreData.BAD, difbad, this.getIcon(difbad)),
      MISS: this.createScoreDetail(this.ScoreData.MISS, difmiss, this.getIcon(difmiss)),
      COMBO: this.createScoreDetail(this.ScoreData.COMBO, difcombo, this.getIcon(difcombo, false)),
      SCORE: this.createScoreDetail(this.ScoreData.SCORE, difscore, this.getIcon(difscore, false)),
      HIGHSCORE: this.createScoreDetail(this.ScoreData.HIGHSCORE, difhighscore, this.getIcon(difhighscore, false)),
      URPM: this.createScoreDetail(this.ScoreData.URPM, difurpm, this.getIcon(difurpm, false)),
      RPM: this.createScoreDetail(this.ScoreData.RPM, difrpm, this.getIcon(difrpm, false)),
      allnotes: this.allnotes
    };
  }

  createScoreDetail(value, diff, icon, calculateRate = true) {
    return {
      value: value,
      rate: calculateRate ? ((value / this.allnotes) * 100).toFixed(2) : undefined,
      diff: diff,
      icon: icon
    };
  }

  getIcon(diff) {
    if (diff > 0) {
      return allowupsrc;
    } else if (diff < 0) {
      return allowdownsrc;
    } else {
      return alowflatsrc;
    }
  }
}

export default ScoreInfo;
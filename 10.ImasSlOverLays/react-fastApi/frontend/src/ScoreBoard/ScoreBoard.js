import React, { useEffect, useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { Card, Typography, CardMedia } from '@mui/material';
import Grid from '@mui/material/Grid2';
import MyresponsiveLine from './MyResponsiveLine';

const ScoreBoard = ({ SongData, ScoreData, RecordsData }) => {
  // Muiマテリアル関連
  const theme = createTheme({
    palette: {
      mode: 'light',
    }
  })
  //Pageレイアウト変数
  const pagewidth = 1300;
  const pageheight = 1000;
  //-------------------------------------
  //JSONデータ処理領域
  // 曲情報
  const [songInfo, setSongInfo] = useState(null);
  useEffect(() => {
    // SongDataの変更を監視して状態を更新
    setSongInfo({
      name: SongData.Name,
      image: SongData.SongImage,
      selectedlevel: SongData.SelectedLevel
    });
  }, [SongData]);
  //スコア情報
  const [scoreInfo, setScoreInfo] = useState(null);
  // 最新レコード情報
  const [latestRecord, setLatestRecord] = useState(null);
  const allowupsrc = '/assets/icon/arrowUp.png';
  const allowdownsrc = '/assets/icon/arrowDown.png';
  const alowflatsrc = '/assets/icon/arrowFlat.png';
  // artistNameを改行で分割
  const ScoreDivision = ['PERFECT', 'GREAT', 'NICE', 'BAD', 'MISS'];
  useEffect(() => {
    // ScoreDataの変更を監視して状態を更新
    // RecordsDataから最新のレコードを抽出
    const latest = RecordsData.reduce((latest, record) => {
      return new Date(record.Date) > new Date(latest.Date) ? record : latest;
    }, RecordsData[0]);
    setLatestRecord(latest);
    //　スコア情報を更新
    const allnotes = ScoreData.PERFECT + ScoreData.GREAT + ScoreData.NICE + ScoreData.BAD + ScoreData.MISS;
    if (!latestRecord) {
      /*最新レコードがない場合*/
      setScoreInfo({
        PERFECT: {
          value: ScoreData.PERFECT,
          rate: ((ScoreData.PERFECT / allnotes) * 100).toFixed(2),
          diff: 0,
          icon: alowflatsrc
        },
        GREAT: {
          value: ScoreData.GREAT,
          rate: ((ScoreData.GREAT / allnotes) * 100).toFixed(2),
          diff: 0,
          icon: alowflatsrc
        },
        NICE: {
          value: ScoreData.NICE,
          rate: ((ScoreData.NICE / allnotes) * 100).toFixed(2),
          diff: 0,
          icon: alowflatsrc
        },
        BAD: {
          value: ScoreData.BAD,
          rate: ((ScoreData.BAD / allnotes) * 100).toFixed(2),
          diff: 0,
          icon: alowflatsrc
        },
        MISS: {
          value: ScoreData.MISS,
          rate: ((ScoreData.MISS / allnotes) * 100).toFixed(2),
          diff: 0,
          icon: alowflatsrc
        },
        COMBO: {
          value: ScoreData.COMBO,
          diff: 0,
          icon: alowflatsrc
        },
        SCORE: {
          value: ScoreData.SCORE,
          diff: 0,
          icon: alowflatsrc
        },
        HIGHSCORE: {
          value: ScoreData.HIGHSCORE,
          diff: 0,
          icon: alowflatsrc
        },
        URPM: {
          value: ScoreData.URPM,
          diff: 0,
          icon: alowflatsrc
        },
        RPM: {
          value: ScoreData.RPM,
          diff: 0,
          icon: alowflatsrc
        },
        allnotes: allnotes
      });
    } else {
      /*最新レコードがある場合*/
      const difperfect = ScoreData.PERFECT - latestRecord.Perfect;
      const difgreat = ScoreData.GREAT - latestRecord.Great;
      const difnice = ScoreData.NICE - latestRecord.Nice;
      const difbad = ScoreData.BAD - latestRecord.Bad;
      const difmiss = ScoreData.MISS - latestRecord.Miss;
      const difcombo = ScoreData.COMBO - latestRecord.Combo;
      const difscore = ScoreData.SCORE - latestRecord.Score;
      const difhighscore = ScoreData.HIGHSCORE - latestRecord.HighScore;
      const difurpm = ScoreData.URPM - latestRecord.URPM;
      const difrpm = ScoreData.RPM - latestRecord.RPM;
      /*差分アイコンの設定*/
      if (difperfect > 0) {
        var srcperfecticon = allowupsrc;
      } else if (difperfect < 0) {
        var srcperfecticon = allowdownsrc;
      } else {
        var srcperfecticon = alowflatsrc;
      }
      if (difgreat > 0) {
        var srcgreaticon = allowupsrc;
      } else if (difgreat < 0) {
        var srcgreaticon = allowdownsrc;
      } else {
        var srcgreaticon = alowflatsrc;
      }
      if (difnice > 0) {
        var srcniceicon = allowupsrc;
      } else if (difnice < 0) {
        var srcniceicon = allowdownsrc;
      } else {
        var srcniceicon = alowflatsrc;
      }
      if (difbad > 0) {
        var srcbadicon = allowupsrc;
      } else if (difbad < 0) {
        var srcbadicon = allowdownsrc;
      } else {
        var srcbadicon = alowflatsrc;
      }
      if (difmiss > 0) {
        var srcmissicon = allowupsrc;
      } else if (difmiss < 0) {
        var srcmissicon = allowdownsrc;
      } else {
        var srcmissicon = alowflatsrc;
      }
      if (difcombo > 0) {
        var srccomboicon = allowupsrc;
      } else if (difcombo < 0) {
        var srccomboicon = allowdownsrc;
      } else {
        var srccomboicon = alowflatsrc;
      }
      if (difscore > 0) {
        var srcscoreicon = allowupsrc;
      } else if (difscore < 0) {
        var srcscoreicon = allowdownsrc;
      } else {
        var srcscoreicon = alowflatsrc;
      }
      if (difhighscore > 0) {
        var srchighscoreicon = allowupsrc;
      } else if (difhighscore < 0) {
        var srchighscoreicon = allowdownsrc;
      } else {
        var srchighscoreicon = alowflatsrc;
      }
      if (difurpm > 0) {
        var srcurpmicon = allowupsrc;
      } else if (difurpm < 0) {
        var srcurpmicon = allowdownsrc;
      } else {
        var srcurpmicon = alowflatsrc;
      }
      if (difrpm > 0) {
        var srcrpmicon = allowupsrc;
      } else if (difrpm < 0) {
        var srcrpmicon = allowdownsrc;
      } else {
        var srcrpmicon = alowflatsrc;
      }
      setScoreInfo({
        PERFECT: {
          value: ScoreData.PERFECT,
          rate: ((ScoreData.PERFECT / allnotes) * 100).toFixed(2),
          diff: difperfect,
          icon: srcperfecticon
        },
        GREAT: {
          value: ScoreData.GREAT,
          rate: ((ScoreData.GREAT / allnotes) * 100).toFixed(2),
          diff: difgreat,
          icon: srcgreaticon
        },
        NICE: {
          value: ScoreData.NICE,
          rate: ((ScoreData.NICE / allnotes) * 100).toFixed(2),
          diff: difnice,
          icon: srcniceicon
        },
        BAD: {
          value: ScoreData.BAD,
          rate: ((ScoreData.BAD / allnotes) * 100).toFixed(2),
          diff: difbad,
          icon: srcbadicon
        },
        MISS: {
          value: ScoreData.MISS,
          rate: ((ScoreData.MISS / allnotes) * 100).toFixed(2),
          diff: difmiss,
          icon: srcmissicon
        },
        COMBO: {
          value: ScoreData.COMBO,
          diff: difcombo,
          icon: srccomboicon
        },
        SCORE: {
          value: ScoreData.SCORE,
          diff: difscore,
          icon: srcscoreicon
        },
        HIGHSCORE: {
          value: ScoreData.HIGHSCORE,
          diff: difhighscore,
          icon: srchighscoreicon
        },
        URPM: {
          value: ScoreData.URPM,
          diff: difurpm,
          icon: srcurpmicon
        },
        RPM: {
          value: ScoreData.RPM,
          diff: difrpm,
          icon: srcrpmicon
        },
        allnotes: allnotes
      });
    }
  }, [RecordsData, ScoreData]);
  if (!songInfo && !scoreInfo) {
    return <div>データがありません</div>;
  } else {
    return (
      <ThemeProvider theme={theme}>
        <Grid container spacing={2} sx={{ width: pagewidth, height: pageheight, display: 'flex', flexDirection: 'column', backgroundColor: 'rgb(250, 250, 251)', padding: 1, 'font-family': 'Open Sans, sans-serif', color: '#111', 'font-weight': '200' }}>
          <Grid container spacing={2} sx={{ width: pagewidth, height: 70, display: 'flex' }}>
            {/*楽曲画像表示*/}
            <Card sx={{ display: 'flex' }}>
              <CardMedia
                component="img"
                sx={{ width: 70, height: 70, objectFit: 'contain' }}
                src={songInfo.image}
                alt="songimage"
              />
            </Card>
            {/* 楽曲情報表示 */}
            <Grid sx={{ display: 'flex', 'margin-left': '10px', flexDirection: 'column' }}>
              <Typography variant="subtitle1" gutterBottom>
                {songInfo.selectedlevel}
              </Typography>
              <Typography variant="h5" gutterBottom>
                {songInfo.name}
              </Typography>
            </Grid>
          </Grid>

          {/* スコア情報表示 */}
          <Grid container spacing={2} sx={{ width: '100%', height: 100, display: 'flex' }}>
            {ScoreDivision.map((line, index) => {
              const scoredivisionname = line;
              const scoredivisionvalue = scoreInfo[scoredivisionname];
              return (
                <Card sx={{ padding: 1, flexGrow: 1 }}>
                  <Grid sx={{ display: 'flex', flexDirection: 'column' }}>
                    <Typography variant="subtitle1" gutterBottom>
                      {scoredivisionname}
                    </Typography>
                    <Grid sx={{ display: 'flex' }}>
                      <Grid>
                        <Typography variant="h6" gutterBottom>
                          {scoredivisionvalue.value}
                        </Typography>
                      </Grid>
                      <Grid textAlign={"end"} sx={{ width: '100%' }}>
                        <Typography variant="h6">
                          {scoredivisionvalue.rate}%
                        </Typography>
                      </Grid>
                    </Grid>
                    <Grid height={50}>
                      <MyresponsiveLine data={setScoreInfo} />
                    </Grid>
                  </Grid>
                </Card>
              );
            })}
          </Grid>
        </Grid>
      </ThemeProvider>
    )
  }
}
export default ScoreBoard;
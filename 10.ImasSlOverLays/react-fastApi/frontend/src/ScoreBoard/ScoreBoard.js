import React, { useEffect, useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { Card, Typography, CardMedia } from '@mui/material';
import Grid from '@mui/material/Grid2';
import MyresponsiveLine from './MyResponsiveLine';
import ScoreInfo from './ScoreInfo'; // ScoreInfoクラスをインポート
import RecordInfo from './RecordInfo'; // RecordInfoクラスをインポート
import generateScoreData from './generateScoreData'; // データ生成関数をインポート

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
  // スコア情報
  const [scoreInfo, setScoreInfo] = useState(null);
  // レコード情報
  const [recordInfo, setRecordInfo] = useState(null);
  // 最新のレコード
  const [latestRecord, setLatestRecord] = useState(null);
  // グラフ用データ
  const [graphData, setGraphData] = useState([]);

  // songDataの変更を監視して状態を更新
  useEffect(() => {
    setSongInfo({
      name: SongData.Name,
      image: SongData.SongImage,
      selectedlevel: SongData.SelectedLevel
    });
  }, [SongData]);

  // RecordsDataから最新のレコードを抽出
  useEffect(() => {
    const latest = RecordsData.reduce((latest, record) => {
      return new Date(record.Date) > new Date(latest.Date) ? record : latest;
    }, RecordsData[0]);
    setLatestRecord(latest);
  }, [RecordsData]);

  // スコア情報の更新
  useEffect(() => {
    if (latestRecord) {
      const scoreInfoInstance = new ScoreInfo(ScoreData, latestRecord);
      setScoreInfo(scoreInfoInstance.info);
    }
  }, [latestRecord, ScoreData, RecordsData]);

  // レコード情報の更新
  useEffect(() => {
    const recordInfoInstance = new RecordInfo(RecordsData);
    setRecordInfo(recordInfoInstance);
  }, [RecordsData]);

  // // グラフ用データの生成
  // useEffect(() => {
  //   if (recordInfo) {
  //     const fields = ['PERFECT', 'GREAT', 'NICE', 'BAD', 'MISS'];
  //     setGraphData(generateScoreData(recordInfo, fields));
  //     console.log('GraphData:', graphData); // デバッグ用
  //   }
  // }, [recordInfo]);

  if (!songInfo && !scoreInfo) {
    return (
      <div>データがありません</div>
    );
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
            {scoreInfo && ['PERFECT', 'GREAT', 'NICE', 'BAD', 'MISS'].map((line, index) => {
              const scoredivisionname = line;
              const scoredivisionvalue = scoreInfo[scoredivisionname];
              const graphData = generateScoreData(recordInfo, scoredivisionname, 20);
              // カードの背景色を線形グラデーションに設定
              let cardBackground;
              switch (line) {
                case 'PERFECT':
                  cardBackground = 'linear-gradient(-225deg, #2CD8D5 0%, #C5C1FF 56%, #FFBAC3 100%)';
                  break;
                case 'GREAT':
                  cardBackground = 'linear-gradient(to top, #ff9a9e 0%, #fecfef 99%, #fecfef 100%)';
                  break;
                case 'NICE':
                  cardBackground = 'linear-gradient(120deg, #f6d365 0%, #fda085 100%)';
                  break;
                case 'BAD':
                  cardBackground = 'linear-gradient(to right, #4facfe 0%, #00f2fe 100%)';
                  break;
                case 'MISS':
                  cardBackground = 'linear-gradient(to right, #43e97b 0%, #38f9d7 100%)';
                  break;
                default:
                  cardBackground = 'linear-gradient(90deg, rgba(187, 255, 239, 1), rgba(236, 237, 203, 1) 34%, rgba(248, 227, 183, 1) 72%, rgba(255, 155, 252, 1) 97%)';
              }
              return (
                <Card key={index} sx={{ padding: 1, flexGrow: 1 , background: cardBackground ,color:'white'}}>
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
                      <MyresponsiveLine data={graphData} />
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
import React, { useRef, useEffect, useState } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { CSSTransition } from 'react-transition-group'
import "./App.css";
//自作コンポーネントのインポート
import NormalContent from './components/NormalContent';
import ImasCard from './components/ImasCard';
import { MusicInfo } from "./cards";
import { ScoreBoard } from "./ScoreBoard";


const STATE_NORMAL = 'normal';
const STATE_SELECT_SONG = 'select_song';
const STATE_SHOW_SCORE = 'show_score';

function App() {
  const [currentState, setCurrentState] = useState('normal');
  const [songInfo, setSongInfo] = useState(null);
  const [recordInfo, setRecordInfo] = useState(null);
  const [scoreInfo, setScoreInfo] = useState(null);
  const [inProp, setInProp] = useState(true);

  useEffect(() => {
    // WebSocketメッセージ受信時の処理
    const ws = new WebSocket('ws://localhost:8000/ws');
    ws.onmessage = async (event) => {
      const data = event.data;
      setInProp(false); // フェードアウト開始
      setTimeout(async () => {
        // fastapiから送信される状態に基づいてcurrentStateを更新
        if (data === 'normal') {
          setCurrentState(STATE_NORMAL);
        } else if (data === 'select_song') {
          try {
            // 選択楽曲情報取得
            const songInfoResponse = await fetch('http://localhost:8000/public/data/songInfo.json', {
              cache: 'no-store'
            });
            const songInfoData = await songInfoResponse.json();
            setSongInfo(songInfoData);
            // レコード情報取得
            const recordInfoResponse = await fetch('http://localhost:8000/public/data/recordInfo.json', {
              cache: 'no-store'
            });
            const recordInfoData = await recordInfoResponse.json();
            setRecordInfo(recordInfoData);
            // currentStateをselect_songに更新        
            setCurrentState(STATE_SELECT_SONG);
          } catch (error) {
            console.error('Error fetching data:', error);
          }
        } else if (data === 'show_score') {
          // スコア情報取得
          const scoreInfoResponse = await fetch('http://localhost:8000/public/data/scoreInfo.json', {
            cache: 'no-store'
          });
          const recordInfoData = await scoreInfoResponse.json();
          setScoreInfo(recordInfoData);
          // currentStateをshow_scoreに更新
          setCurrentState(STATE_SHOW_SCORE);
        }
        setInProp(true); // フェードイン開始
      }, 500); // フェードアウトの時間と一致させる
    };
    return () => {
      ws.close();
    };
  }, []);

  const contentMap = {
    [STATE_NORMAL]: (
      <div>
        <ImasCard />
        <NormalContent />
      </div>
    ),
    [STATE_SELECT_SONG]: (
      <div>
        <ImasCard />
        <MusicInfo data={songInfo} />
      </div>
    ),
    [STATE_SHOW_SCORE]: (
      <div style={{
        display: 'flex',
        'justify-content': 'center',
        'align-items': 'center',
        width: '100vw',
        height: '100vh'
      }}>
        <ScoreBoard ScoreData={scoreInfo} RecordsData={recordInfo} SongData={songInfo} />
      </div>
    )
  };

  return (
    <CSSTransition in={inProp} timeout={500} classNames="fade">
      <div style={{ width: "1920px", height: "1080px" }}>
        {contentMap[currentState] || null}
      </div>
    </CSSTransition>
  );
}
export default App;
import React, { useRef, useEffect, useState} from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
//各種コンポーネントのインポート
import NormalContent from './components/NormalContent';
import ImasCard from './components/ImasCard';
import { MusicInfo } from "./cards";
import "./App.css";

const STATE_NORMAL = 'normal';
const STATE_SELECT_SONG = 'select_song';
const STATE_SHOW_SCORE = 'show_score';

function App() {
  const [currentState, setCurrentState] = useState('normal');
  const [songInfo, setSongInfo] = useState(null);
  const [recordInfo, setRecordInfo] = useState(null);

  useEffect(() => {
    // WebSocketメッセージ受信時の処理
    const ws = new WebSocket('ws://localhost:8000/ws');
    ws.onmessage = async (event) => {
      const data = event.data;
      // fastapiから送信される状態に基づいてcurrentStateを更新
      if (data === 'normal') {
        setCurrentState(STATE_NORMAL);
      } else if (data === 'select_song') {
        setCurrentState(STATE_SELECT_SONG);
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
        } catch (error) {
          console.error('Error fetching data:', error);
        }
        setCurrentState(STATE_SHOW_SCORE);
      } else if (data === 'show_score') {
        setCurrentState(STATE_SHOW_SCORE);
      }
    };
    return () => {
      ws.close();
    };
  }, []);

  const contentMap = {
    [STATE_NORMAL]: (
      <div>
        <ImasCard />
        <NormalContent/>
      </div>
    ),
    [STATE_SELECT_SONG]: (
      <div>
        <ImasCard />
        <MusicInfo data={songInfo}/>
      </div>
    ),
    [STATE_SHOW_SCORE]: <p> show score</p>,
  };

  return (
    <div style={{ width: "1920px", height: "1080px" }}>
      {contentMap[currentState] || null}
    </div>
  );
}
export default App;
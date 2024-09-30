import React, { useRef, useEffect } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { CardHighlight } from "./mui-treasury/card-highlight/CardHighlight.tsx";
// Swiperコンポーネントをインポート
import { Swiper, SwiperSlide } from "swiper/react";
import SwiperCore from "swiper";
import { Autoplay, Pagination, Navigation } from "swiper/modules";
import "swiper/swiper-bundle.css";
// Import Swiper styles
import "swiper/css";
import "swiper/css/pagination";
import "swiper/css/navigation";
import "./App.css";
import { AboutMe, AboutMeJa, AboutImas, AboutImasOverLay } from "./cards";

SwiperCore.use([Autoplay]);

function App() {
  useEffect(() => {
    // 状態を定義
    const STATE_NORMAL = 'normal';
    const STATE_SELECT_SONG = 'select_song';
    const STATE_SHOW_SCORE = 'show_score';
    let currentState = STATE_NORMAL;
    // document.querySelector('.NormalSwiper').classList.add('fade-out');
    // WebSocketメッセージ受信時の処理
    const ws = new WebSocket('ws://localhost:8000/ws');
    ws.onmessage = (event) => {
      const data = event.data;
      // fastapiから送信される状態に基づいてcurrentStateを更新
      if (data === 'normal') {
        currentState = STATE_NORMAL;
      } else if (data === 'select_song') {
        currentState = STATE_SELECT_SONG;
      } else if (data === 'show_score') {
        currentState = STATE_SHOW_SCORE;
      }
      // 状態に応じた処理
      switch (currentState) {
        case STATE_NORMAL:
          console.log('通常時の処理を実行');
          // 通常時の処理をここに追加
          break;
        case STATE_SELECT_SONG:
          console.log('曲選択時の処理を実行');
          // 曲選択時の処理をここに追加
          break;
        case STATE_SHOW_SCORE:
          console.log('スコア表示時の処理を実行');
          // スコア表示時の処理をここに追加
          break;
        default:
          console.log('未知の状態');
      }
    };
    return () => {
      ws.close();
    };
  }, []);
  const progressCircle = useRef(null);
  const progressContent = useRef(null);
  const onAutoplayTimeLeft = (s, time, progress) => {
    progressCircle.current.style.setProperty("--progress", 1 - progress);
    progressContent.current.textContent = `${Math.ceil(time / 1000)}s`;
  };
  return (
    <div style={{ width: "1920px", height: "1080px" }}>
      {/* アイドルマスターシンデレラガールズ　カード */}
      <div style={{ position: "absolute", left: 0, bottom: 0 }}>
        <CardHighlight />
      </div>
      <div
        style={{
          position: "absolute",
          left: "335px",
          bottom: 0,
          height: "230px",
          width: "1140px",
        }}
      >
        {/* 楽曲未選択時スワイプ */}
        <Swiper
          class="NormalSwiper"
          modules={[Autoplay]}
          autoplay={{ delay: 60000 }}
          onAutoplayTimeLeft={onAutoplayTimeLeft}
        >
          <SwiperSlide>
            <AboutMe />
          </SwiperSlide>
          <SwiperSlide>
            <AboutMeJa />
          </SwiperSlide>
          <SwiperSlide>
            <AboutImas />
          </SwiperSlide>
          <SwiperSlide>
            <AboutImasOverLay />
          </SwiperSlide>
          <div className="autoplay-progress" slot="container-end"
            style={{ position: 'absolute', right: '0px', bottom: '200px', zIndex: '20' }}>
            <svg viewBox="0 0 48 48" ref={progressCircle}>
              <circle cx="24" cy="24" r="20"></circle>
            </svg>
            <span ref={progressContent}></span>
          </div>
        </Swiper>
      </div>
    </div>
  );
}

export default App;

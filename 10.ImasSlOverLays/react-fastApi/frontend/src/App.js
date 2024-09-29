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
    const ws = new WebSocket("ws://localhost:8000/ws");
    ws.onmessage = (event) => {
      if (event.data === "redirect") {
        // window.location.href = '/init';
      }
      console.log(event.data);
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
      <div
        style={{
          position: "absolute",
          left: "335px",
          bottom: 0,
          height: "230px",
          width: "1140px",
        }}
      >
        <Swiper
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
            style={{position: 'absolute', right:'0px', bottom: '200px',zIndex:'20'}}>
            <svg viewBox="0 0 48 48" ref={progressCircle}>
              <circle cx="24" cy="24" r="20"></circle>
            </svg>
            <span ref={progressContent}></span>
          </div>
        </Swiper>
      </div>
      <div style={{ position: "absolute", left: 0, bottom: 0 }}>
        <CardHighlight />
      </div>
    </div>
  );
}

export default App;

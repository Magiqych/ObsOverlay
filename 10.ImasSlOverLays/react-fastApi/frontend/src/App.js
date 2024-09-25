import React, { useEffect } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { CardHighlight } from "./mui-treasury/card-highlight/CardHighlight.tsx";
// Swiperコンポーネントをインポート
import { Swiper, SwiperSlide } from 'swiper/react';
import SwiperCore from 'swiper';
import { Autoplay } from 'swiper/modules';
import 'swiper/swiper-bundle.css';
import "./App.css";
import InitPage from "./page/InitPage";
import { Card } from "@mui/material";
import Typography from "@mui/material/Typography";
import { AboutMe ,AboutMeJa} from './cards';
SwiperCore.use([Autoplay]);

function App() {
  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws");
    ws.onmessage = (event) => {
      if (event.data === "redirect") {
        // window.location.href = '/init';
      }
    };
    return () => {
      ws.close();
    };
  }, []);
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
          autoplay={{ delay: 10000 }}
        >
          <SwiperSlide>
            <AboutMe/>
          </SwiperSlide>
          <SwiperSlide>
            <AboutMeJa/>
          </SwiperSlide>
          <SwiperSlide>
            <Card sx={{ Width: "1000px" }}>
              <div width="900px" height="200px">
                <Typography variant="h5" component="h2">
                  Side1
                </Typography>
              </div>
            </Card>
          </SwiperSlide>
          <SwiperSlide>
            <Card sx={{ Width: "1000px" }}>
              <div width="900px" height="200px">
                <Typography variant="h5" component="h2">
                  Side1
                </Typography>
              </div>
            </Card>
          </SwiperSlide>
          <SwiperSlide>
            <Card sx={{ Width: "1000px" }}>
              <div width="900px" height="200px">
                <Typography variant="h5" component="h2">
                  Side1
                </Typography>
              </div>
            </Card>
          </SwiperSlide>
          <SwiperSlide>
            <Card sx={{ Width: "1000px" }}>
              <div width="900px" height="200px">
                <Typography variant="h5" component="h2">
                  Side1
                </Typography>
              </div>
            </Card>
          </SwiperSlide>
          <SwiperSlide>
            <Card sx={{ Width: "1000px" }}>
              <div width="900px" height="200px">
                <Typography variant="h5" component="h2">
                  Side1
                </Typography>
              </div>
            </Card>
          </SwiperSlide>
          {/* 必要に応じてスライドを追加 */}
        </Swiper>
      </div>
      <div style={{ position: "absolute", left: 0, bottom: 0 }}>
        <CardHighlight />
      </div>
    </div>
  );
}

export default App;

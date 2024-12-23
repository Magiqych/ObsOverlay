import React, { useRef } from 'react';
//カードモジュールのインポート
import { AboutMe, AboutMeJa, AboutImas } from "../cards";
//import { AboutMe, AboutMeJa, AboutImas, AboutImasOverLay } from "./cards";
// import AboutImasOverLay from './cards/AboutImasOverLay';
//Swiperのインポート
import { Swiper, SwiperSlide } from "swiper/react";
import SwiperCore from "swiper";
import { Autoplay, Pagination, Navigation } from "swiper/modules";
import "swiper/swiper-bundle.css";
// Import Swiper styles
import "swiper/css";
import "swiper/css/pagination";
import "swiper/css/navigation";

SwiperCore.use([Autoplay]);

const NormalContent = () => {
    const progressCircle = useRef(null);
    const progressContent = useRef(null);
    const onAutoplayTimeLeft = (s, time, progress) => {
        progressCircle.current.style.setProperty("--progress", 1 - progress);
        progressContent.current.textContent = `${Math.ceil(time / 1000)}s`;
    };
    return (
        <div
            style={{
                position: "absolute",
                left: "350px",
                bottom: 0,
                height: "230px",
                width: "1140px",
            }}
        >
            {/* スワイパー */}
            <Swiper
                className="NormalSwiper"
                modules={[Autoplay]}
                autoplay={{ delay: 60000 }}
                onAutoplayTimeLeft={onAutoplayTimeLeft}
                loop={true}
                slidesPerView={1}
                spaceBetween={500}
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
                {/* <SwiperSlide>
                    <AboutImasOverLay />
                    </SwiperSlide> */}
                <div className="autoplay-progress" slot="container-end"
                    style={{ position: 'absolute', right: '0px', bottom: '180px' }}>
                    <svg viewBox="0 0 48 48" ref={progressCircle}>
                        <circle cx="24" cy="24" r="20"></circle>
                    </svg>
                    <span ref={progressContent}></span>
                </div>
            </Swiper>
        </div>
    );
};

export default NormalContent;
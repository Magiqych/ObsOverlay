import * as React from "react";
import { Card, CardContent, Typography, Box, Stack } from "@mui/material";
// Swiperコンポーネントをインポート
import { Swiper, SwiperSlide } from "swiper/react";
import SwiperCore from "swiper";
import { Autoplay } from "swiper/modules";
import "swiper/swiper-bundle.css";
import { useTheme } from "@mui/material/styles";
import "./AboutImasOverLay.css";

SwiperCore.use([Autoplay]);

export default function AboutImasOverLay() {
  const theme = useTheme();
  return (
    <Card>
      <CardContent>
        <Stack direction="column" spacing={0}>
          <Typography
            variant="h6"
            component="h2"
            sx={{ color: "text.secondary" }}
          >
            ImasOverlay@Developing@Magiqych powered by...
          </Typography>
          <Swiper
            modules={[Autoplay]}
            autoplay={{delay: 0}}
            loop={true}
            freeMode={true}
            freemodefluid={true}
            allowTouchMove={false}
            spaceBetween={32}
            speed={4000}
            centeredSlides={true}
            navigation={false}
            pagination={false}
            slidesPerView={3}
            // noSwipingClass="swiper-no-swiping"
            style={{ width: "100%", height: "auto" }}
          >
            <SwiperSlide>
            <Box
                component="img"
                alt="fastAPI"
                src={"/assets/static/fastAPI.png"}
                sx={{ width: "400px", height: "180px", objectFit: "contain" }}
              />
            </SwiperSlide>
            <SwiperSlide>
              <Box
                component="img"
                alt="pytesseract"
                src={"/assets/static/pytesseract.png"}
                sx={{ width: "400px", height: "180px", objectFit: "contain" }}
              />
            </SwiperSlide>
            <SwiperSlide>
              <Box
                component="img"
                alt="TensorFlow"
                src={"/assets/static/TensorFlow.png"}
                sx={{ width: "400px", height: "180px", objectFit: "contain" }}
              />
            </SwiperSlide>
            <SwiperSlide>
              <Box
                component="img"
                alt="opencv"
                src={"/assets/static/opencv.png"}
                sx={{ width: "400px", height: "180px", objectFit: "contain" }}
              />
            </SwiperSlide>
            <SwiperSlide>
              <Box
                component="img"
                alt="reactmuitailwind"
                src={"/assets/static/reactmuitailwind.jpg"}
                sx={{ width: "400px", height: "180px", objectFit: "contain" }}
              />
            </SwiperSlide>
            <SwiperSlide>
              <Box
                component="img"
                alt="storybook"
                src={"/assets/static/storybook.webp"}
                sx={{ width: "400px", height: "180px", objectFit: "contain" }}
              />
            </SwiperSlide>
            <SwiperSlide>
              <Box
                component="img"
                alt="vs-code-logo"
                src={"/assets/static/vs-code-logo.png"}
                sx={{ width: "400px", height: "180px", objectFit: "contain" }}
              />
            </SwiperSlide>
            <SwiperSlide>
              <Box
                component="img"
                alt="sqlite"
                src={"/assets/static/SQLite_logo.png"}
                sx={{ width: "400px", height: "180px", objectFit: "contain" }}
              />
            </SwiperSlide>
            <SwiperSlide>
              <Box
                component="img"
                alt="playwrite"
                src={"/assets/static/playwrite.png"}
                sx={{ width: "400px", height: "180px", objectFit: "contain" }}
              />
            </SwiperSlide>
          </Swiper>
        </Stack>
      </CardContent>

      <Box
        sx={{
          position: "fixed",
          bottom: 16,
          right: 20,
          backgroundColor: "#455a64",
          color: "white",
          borderRadius: 2,
          padding: 1,
          boxShadow: 3,
          zIndex: 1000,
        }}
      >
        <Typography variant="body2">
          © 2024 Magiqych All rights reserved. | ImasOverlay
        </Typography>
      </Box>
    </Card>
  );
}

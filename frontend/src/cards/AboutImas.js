import * as React from "react";
import { Card, CardContent, Typography, Box, Stack } from "@mui/material";
// Swiperコンポーネントをインポート
import { Swiper, SwiperSlide } from "swiper/react";
import SwiperCore from "swiper";
import { Autoplay } from "swiper/modules";
import "swiper/swiper-bundle.css";
import { useTheme } from '@mui/material/styles';

SwiperCore.use([Autoplay]);

export default function AboutImas() {
  const theme = useTheme();
  return (
    <Card>
      <Swiper
        modules={[Autoplay]}
        autoplay={{ delay: 2000 }}
        slidesPerView={3}
        spaceBetween={30}
        height="150px"
      >
        <SwiperSlide>
          <Box
            component="img"
            alt="1stLaunch"
            src={"/assets/static/20111128_1_pic_01.png"}
            sx={{ width: "400px", height: "100px", objectFit: "contain" }}
          />
        </SwiperSlide>
        <SwiperSlide>
          <Box
            component="img"
            alt="2ndLaunch"
            src={"/assets/static/20150903_1_pic_01.png"}
            sx={{ width: "400px", height: "100px", objectFit: "contain" }}
          />
        </SwiperSlide>
        <SwiperSlide>
          <Box
            component="img"
            alt="10thAnniversary"
            src={"/assets/static/20211128_1_pic_01.png"}
            sx={{ width: "400px", height: "100px", objectFit: "contain" }}
          />
        </SwiperSlide>
      </Swiper>
      <CardContent>
        <Stack direction="row" spacing={0}>
          <Box
            component="img"
            alt="gamelogo"
            src={"/assets/static/GameLogo.webp"}
            sx={{ width: "100px", height: "100px", objectFit: "contain" }}
          />
          <Box
            component="img"
            alt="qr"
            src={"/assets/static/app_qr.png"}
            sx={{ width: "100px", height: "100px", objectFit: "contain" }}
          />
          <Typography
            variant="h6"
            component="h2"
            sx={{ color: "text.secondary" }}
          >
            2011年11月28日「アイドルマスター シンデレラガールズ」リリース
            <br />
            2015年09月03日「アイドルマスター シンデレラガールズ
            スターライトステージ」リリース
            <br />
            2021年11月28日 シンデレラガールズ10周年
          </Typography>
        </Stack>
      </CardContent>
      
      <Box
        sx={{
          position: 'fixed',
          bottom: 15,
          right: 15,
          backgroundColor: '#455a64',
          color: 'white',
          borderRadius: 2,
          padding: 1,
          boxShadow: 3,
        }}
      >
        <Typography variant="body2">
          THE IDOLM@STER™& ©Bandai Namco Entertainment Inc.
        </Typography>
      </Box>
    </Card>
  );
}

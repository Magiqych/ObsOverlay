import React from "react";
import { Container, createTheme, ThemeProvider } from "@mui/material";
import { CardHighlight } from "../mui-treasury/card-highlight/CardHighlight.tsx";
import "./InitPage.css"; // CSSファイルをインポート

function InitPage() {
  return (
    <div style={{width:'1920px',height:'1080px'}}>
      <div style={{ position: "absolute", left: 0,bottom:0,height:'200px',width:'600px',backgroundColor:'red' }}>
      
      </div>
      <div style={{ position: "absolute", left: 0, bottom: 0 }}>
        <CardHighlight />
      </div>
    </div>
  );
}

export default InitPage;

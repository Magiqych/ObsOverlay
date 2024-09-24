import "./App.css";
import { Container, Typography } from "@mui/material";  // MUIのコンポーネントをインポート
import { BrowserRouter } from "react-router-dom";
import { Router } from "./router/Router";
import { Toaster } from "react-hot-toast";
import { RecoilRoot } from "recoil";
import { useState, useEffect } from "react";
import axios from 'axios';

// Point Eel web socket to the instance
export const eel = window.eel;
eel.set_host('ws://localhost:8080');

interface Message {
  name: string;
  image: string;
}
// src/main.js

// JavaScript側で関数を定義
function receive_message(messagebody: any) {
  console.log("Received message:", messagebody);
  // ここでメッセージを処理するコードを追加
}

// Eelに関数を公開
eel.expose(receive_message, 'receive_message');

function App() {
  const [message, setMessage] = useState<Message | null>(null);

  useEffect(() => {
    function receive_message(messagebody: Message) {
      setMessage(messagebody);
    }
    eel.expose(receive_message, 'receive_message');
  }, []);

  return (
    <RecoilRoot>
      <BrowserRouter>
        <Router />
      </BrowserRouter>
      <Toaster />
      <Container>
        {message && (
          <div>
            <Typography variant="h5">{message.name}</Typography>
            <img src={message.image} alt={message.name} />
          </div>
        )}
      </Container>
    </RecoilRoot>
  );
}

export default App;
import "./App.css";
import { Container, Typography } from "@mui/material";  // MUIのコンポーネントをインポート
import { BrowserRouter } from "react-router-dom";
import { Router } from "./router/Router";
import { Toaster } from "react-hot-toast";
import { RecoilRoot } from "recoil";
import { useState, useEffect } from "react";

// Point Eel web socket to the instance
export const eel = window.eel
eel.set_host('ws://localhost:8080');

interface Message {
  name: string;
  image: string;
}

function App() {
  const [message, setMessage] = useState<Message | null>(null);

  useEffect(() => {
    function receiveMessage(msg: Message) {
      setMessage(msg);
    }
    window.eel.expose(receiveMessage, 'receive_message');
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
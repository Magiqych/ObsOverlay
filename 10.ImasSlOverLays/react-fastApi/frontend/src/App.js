import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';
import { RecoilRoot } from 'recoil';
import { Toaster } from 'react-hot-toast';
import './App.css';

// WebSocketの初期化
const socket = io('http://localhost:8000');

function App() {
  const [message, setMessage] = useState(null);

  useEffect(() => {
    // WebSocketの接続が開いたときの処理
    console.log('WebSocket connection opened');

    // WebSocketでメッセージを受信したときの処理
    socket.on('message', (data) => {
      setMessage(data);
    });

    // WebSocketの接続が閉じたときの処理
    socket.on('disconnect', () => {
      console.log('WebSocket connection closed');
    });

    // クリーンアップ関数
    return () => {
      socket.off('connect');
      socket.off('message');
      socket.off('disconnect');
    };
  }, [setMessage]);

    // WebSocketでメッセージを受信したときの処理
    socket.on('message', (data) => {
      setMessage(data);
    });

    // WebSocketの接続が閉じたときの処理
    socket.on('disconnect', () => {
      console.log('WebSocket connection closed');
    });

  return (
    <RecoilRoot>
      <Toaster />
      {message && (
        <div>
          <h5>{message.name}</h5>
          <img src={message.image} alt={message.name} />
        </div>
      )}
    </RecoilRoot>
  );
}

export default App;
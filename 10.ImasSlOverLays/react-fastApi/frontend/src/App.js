import React, { useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import InitPage from './page/InitPage';

function App() {
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws');
    ws.onmessage = (event) => {
      if (event.data === 'redirect') {
        window.location.href = '/init';
      }
    };
    return () => {
      ws.close();
    };
  }, []);
  return (
    <Router>
      <Routes>
        <Route path="/init" element={<InitPage />} />
      </Routes>
    </Router>
  );
}

export default App;
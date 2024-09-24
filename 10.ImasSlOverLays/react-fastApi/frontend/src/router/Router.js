import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import Home from '../components/Home'; // 必要に応じてコンポーネントを作成

const Router = () => (
  <BrowserRouter>
    <Switch>
      <Route exact path="/" component={Home} />
      {/* 他のルートを追加 */}
    </Switch>
  </BrowserRouter>
);

export default Router;
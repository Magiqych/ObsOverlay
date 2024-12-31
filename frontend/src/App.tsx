import React from 'react';
import './App.css';
import './styles/classic-stylesheets-master/themes/win9x/theme.css'; // 追加

const App: React.FC = () => {
  return (
    <>
      <div style={{ width: '1920px', height: '1080px', backgroundImage: 'url("./src/assets/background/title.png")', backgroundSize: '1920px 1080px', margin: 0, padding: 0 }} className="win9x">
        <section>
          <div className="example" style={{ width: '1920px', position: 'absolute', top: '940px' }}>
            <div className="flex-row gap">
              <div className="progress-bar" style={{ width: '1920px'}}></div>
            </div>
          </div>
        </section>
      </div>
    </>
  );
}

export default App;
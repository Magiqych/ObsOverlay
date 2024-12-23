import React from 'react';
//カードモジュールのインポート
import { CardHighlight } from "../mui-treasury/card-highlight/CardHighlight.tsx";


const ImasCard = () => {
    return (
        // {/* アイドルマスターシンデレラガールズ　カード */}
        <div style={{ position: "absolute", left: 0, bottom: 0, zIndex: 100 }}>
            <CardHighlight />
        </div>
    );
}
export default ImasCard;
# 流程圖文件 (Flowchart) - 線上算命系統

本文件根據產品需求文件 (PRD) 與系統架構文件 (Architecture) 繪製，詳細呈現使用者在網站上的整體操作流向，以及系統內部的資料互動順序。

## 1. 使用者流程圖（User Flow）

描述使用者從開啟網頁到體驗各項核心功能（抽籤、看紀錄、捐香油錢等）的操作路徑。

```mermaid
flowchart LR
    Start([使用者開啟首頁]) --> CheckAuth{登入狀態？}
    
    CheckAuth -->|未登入| MainMenu[首頁 / 主選單]
    CheckAuth -->|已登入| MainMenu
    
    MainMenu -->|點擊登入/註冊| AuthReq[會員登入/註冊頁面]
    AuthReq -->|成功| MainMenu
    
    MainMenu -->|選擇算命/抽籤| DrawEntry[進入測算畫面]
    DrawEntry --> DoDraw[互動：搖籤或抽卡]
    DoDraw --> ShowResult[顯示測算結果與詳解]
    
    ShowResult --> IsLogin{登入狀態？}
    IsLogin -->|已登入| AutoSave[自動儲存紀錄至個人帳號]
    IsLogin -->|未登入| PromptLogin[提示登入以保存紀錄]
    PromptLogin --> AuthReq
    
    MainMenu -->|查看紀錄| Profile[會員中心]
    Profile --> ProfileList[瀏覽過去歷史紀錄]
    
    MainMenu -->|捐香油錢| DonatePage[香油錢頁面]
    DonatePage --> DonateForm[填寫祈福語與金額]
    DonateForm --> DonatePay[付款/模擬金流畫面]
    DonatePay --> DonateResult[收到感謝語並記錄交易]
```

## 2. 系統序列圖（Sequence Diagram）

以下描述「使用者進行抽籤並將結果存入資料庫」的核心流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (View)
    participant Flask as Flask Route (Controller)
    participant Model as 測算邏輯與模型
    participant DB as SQLite
    
    User->>Browser: 點選「求籤」按鈕
    Browser->>Flask: POST /divination/draw
    Flask->>Model: 呼叫抽取演算法
    Model->>DB: 撈取所有籤詩 (SELECT)
    DB-->>Model: 回傳籤詩清單
    Model-->>Flask: 回傳計算後的結果與詳解
    
    opt 已登入會員 Session 存在
        Flask->>Model: 建立該會員的測算紀錄
        Model->>DB: INSERT INTO records
        DB-->>Model: 寫入成功
    end
    
    Flask-->>Browser: 渲染 result.html 並挾帶結果變數
    Browser-->>User: 顯示最終籤詩內容與解說是
```

## 3. 功能清單對照表

列出系統主要功能對應的路由與 HTTP 方法。

| 功能名稱 | 對應 URL 路徑 | HTTP 方法 | 說明 |
| -------- | ----------- | --------- | ---- |
| 網站首頁 | `/` | GET | 顯示主要介紹、選單入口 |
| 註冊頁面 | `/auth/register` | GET, POST | 呈現註冊表單與處理註冊邏輯 |
| 登入頁面 | `/auth/login` | GET, POST | 呈現登入表單與核對帳密 |
| 登出 | `/auth/logout` | GET (或 POST) | 清除 Session 並導向首頁 |
| 開始測算/抽籤 | `/divination/draw` | GET, POST | 呈現求籤畫面、處置求籤要求 |
| 詳解結果頁 | `/divination/result/<id>` | GET | 讀取特定籤詩或紀錄進行詳細解說 |
| 個人歷史紀錄 | `/profile` | GET | 列出該會員所有測算紀錄清單 |
| 捐獻香油錢表單 | `/donation` | GET | 填寫祈福與金額畫面 |
| 結帳與處理 | `/donation/checkout`| POST | 處理付款模擬、變更交易狀態 |

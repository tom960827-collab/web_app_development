# 線上算命系統 - 流程圖 (Flowchart)

這份文件包含線上算命系統的**使用者流程圖**與核心功能的**系統序列圖**。本設計依據 PRD 與技術架構文件所列的功能需求構建，可以從此圖了解使用者如何在系統內操作，以及資料背後的流動方式。

## 1. 使用者流程圖 (User Flow)

這張圖展示了使用者進入網站後，可能經歷的各項操作路徑，涵蓋：算命/抽籤、註冊登入、查看歷史紀錄、模擬捐款以及結果分享。

```mermaid
flowchart LR
    Start([使用者開啟網站]) --> Home[首頁]
    Home --> Action{要執行什麼操作？}
    
    %% 算命抽籤流程
    Action -->|我要算命/抽籤| Draw[選擇算命項目/抽籤]
    Draw --> FortuneResult[觀看籤詩/算命結果]
    FortuneResult --> IsLoginResult{是否已登入？}
    IsLoginResult -->|是| SaveResult[系統自動儲存紀錄]
    IsLoginResult -->|否| GuestResult[僅顯示但不儲存]
    SaveResult --> Share[分享結果到社群]
    GuestResult --> Share
    SaveResult --> DonateAction
    GuestResult --> DonateAction
    
    %% 捐香油錢流程
    Action -->|想要還願或支持| DonateAction[點擊添香油錢]
    DonateAction --> DonateForm[填寫捐獻金額與心意]
    DonateForm --> FakePayment[模擬付款處理]
    FakePayment --> DonateSuccess[顯示感謝頁面]
    DonateSuccess --> Home
    
    %% 會員流程
    Action -->|會員登入/註冊| Auth{有沒有帳號？}
    Auth -->|沒有| Register[註冊新帳號]
    Auth -->|有| Login[登入]
    Register --> Login
    Login --> Profile[進入個人主頁]
    Profile --> ViewHistory[查看歷史算命/抽籤紀錄]
```

## 2. 系統序列圖 (Sequence Diagram)

此序列圖描述了核心功能「使用者進行抽籤並儲存紀錄」一直到「資料存入 SQLite 資料庫並渲染畫面」的完整系統交互流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask (Controller)
    participant Model as Model (Python)
    participant DB as SQLite (資料庫)
    
    User->>Browser: 點擊「開始抽籤」按鈕
    Browser->>Flask: GET (或 POST) /fortune/draw
    Flask->>Model: 隨機選取抽籤資料/算法
    Model->>DB: 查詢籤詩庫 (SELECT)
    DB-->>Model: 回傳籤詩內容
    Model-->>Flask: 籤詩物件
    
    alt 使用者已登入
        Flask->>Model: 紀錄此次抽籤結果與時間
        Model->>DB: 儲存至個人紀錄表 (INSERT)
        DB-->>Model: 儲存成功
        Model-->>Flask: 紀錄完成
    end
    
    Flask-->>Browser: 使用 Jinja2 渲染抽籤結果頁
    Browser-->>User: 顯示籤詩內容與解讀
```

## 3. 功能清單對照表

以下為 MVP 階段規劃的核心功能，以及其對應的 URL 路徑與 HTTP 方法：

| 功能項目 | URL 路徑 | HTTP 方法 | 說明 |
| :--- | :--- | :--- | :--- |
| **首頁** | `/` | GET | 網站進入點，顯示介紹與主要功能入口。 |
| **註冊頁面** | `/auth/register` | GET, POST | 顯示註冊表單 (GET)，處理註冊邏輯 (POST)。 |
| **登入頁面** | `/auth/login` | GET, POST | 顯示登入表單 (GET)，處理驗證邏輯 (POST)。 |
| **登出處理** | `/auth/logout` | GET | 清除 Session 狀態並登出。 |
| **個人主頁** | `/profile` | GET | 顯示基本資料與過去所有的算命/抽籤歷史紀錄。 |
| **進行抽籤** | `/fortune/draw` | GET, POST | 執行抽籤或算命，並取得結果。 |
| **抽籤結果頁** | `/fortune/result/<id>` | GET | 單一結果的專屬頁面（方便直接分享）。 |
| **捐香油錢** | `/payment/donate` | GET | 顯示香油錢捐獻表單。 |
| **模擬付款** | `/payment/process` | POST | 接收表單並處理模擬付款邏輯，隨後導向成功頁面。 |

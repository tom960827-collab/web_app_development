# 線上算命系統 - 系統架構設計 (Architecture)

這份文件根據 PRD 需求，規劃了線上算命系統的技術架構與資料夾結構，供開發團隊作為後續實作的藍圖。此設計採用輕量且易於擴展的模式，特別適合專案初期的快速迭代。

## 1. 技術架構說明

我們選用的核心技術組合為 **Flask + Jinja2 + SQLite**，並採用類似 MVC（Model-View-Controller）的分層架構來確保程式碼的整潔與好維護。

### 選用技術與原因
- **後端框架 - Flask**：Python 輕量級網頁框架。因為算命系統的重點在於簡單直覺的互動與資料儲存，Flask 足夠輕巧，不會有多餘的負擔，也非常適合中小型專案。
- **模板引擎 - Jinja2**：因為系統不要求完全的前後端分離，採用伺服器端渲染（SSR）可以直接透過 Jinja2 將後端取得的算命結果、籤詩與頁面結合，快速產生 HTML，對初學者友好且載入速度快。
- **資料庫 - SQLite**：輕巧且不須額外架設資料庫伺服器，資料儲存在單一檔案中，適合初期快速開發與驗證 MVP 概念。未來若流量擴大，也很容易轉移到 MySQL 或 PostgreSQL。

### Flask MVC 模式說明
- **Model（模型 / 資料層）**：處理所有與資料庫相關的操作。負責定義會員、算命紀錄、香油錢捐獻紀錄的資料表（Schema），負責建立、讀取、更新和刪除資料。
- **View（視圖 / 顯示層）**：負責畫面渲染與呈現給使用者。這裡指的是 `templates/` 資料夾下的 Jinja2 模板，負責接收 Controller 傳遞下來的資料並顯示。
- **Controller（控制器 / 邏輯層）**：Flask 的 Route (路由) 負責扮演控制器的角色。負責接收使用者的網頁請求（例如點擊「抽籤」）、調用 Model 寫入紀錄、並將結果丟給 View 去渲染。

---

## 2. 專案資料夾結構

為了讓程式碼好管理不混亂，我們將專案依功能模組劃分成以下結構：

```text
web_app_development/
├── app.py                # 應用程式的進入點，負責啟動 Flask 伺服器
├── config.py             # 全域設定檔（如連線加密密鑰、資料庫路徑設定等）
├── requirements.txt      # Python 套件相依清單 (Flask, SQLAlchemy 等)
├── instance/
│   └── database.db       # SQLite 資料庫檔案（不會推送到版控）
├── app/                  # 核心應用程式目錄
│   ├── __init__.py       # 應用程式初始化與設定
│   ├── models/           # (Model) 資料庫模型物件定義
│   │   ├── user.py       # 會員資料模型
│   │   └── record.py     # 算命歷史 / 香油錢紀錄模型
│   ├── routes/           # (Controller) 各頁面路由設定
│   │   ├── auth.py       # 會員註冊、登入相關路由
│   │   ├── fortune.py    # 抽籤、占卜相關路由
│   │   └── payment.py    # 捐香油錢模擬付款路由
│   ├── templates/        # (View) Jinja2 HTML 模板
│   │   ├── base.html     # 網站共用版型（頁首、選單、頁尾）
│   │   ├── index.html    # 首頁
│   │   ├── fortune/      # 抽籤占卜相關的頁面
│   │   ├── auth/         # 登入/註冊的頁面
│   │   └── user/         # 個人紀錄與設定頁面
│   └── static/           # 靜態資源檔案
│       ├── css/          # 樣式表 (style.css)
│       ├── js/           # 客製化互動腳本
│       └── images/       # 網站圖片、籤詩圖片等
└── docs/                 # 專案文件目錄
    ├── PRD.md            # 產品需求文件
    └── ARCHITECTURE.md   # 本文件（系統架構設計）
```

---

## 3. 元件關係圖

以下呈現使用者瀏覽器與系統內部元件的互動方式。

```mermaid
flowchart TD
    Browser[使用者瀏覽器 Browser]
    
    subgraph "Flask Backend System"
        Routes[Routes / Controller\n(app/routes/)]
        Models[Models\n(app/models/)]
        Jinja[Jinja2 Templates / View\n(app/templates/)]
    end
    
    DB[(SQLite Database\n(instance/database.db))]

    %% Request Flow
    Browser -- "1. HTTP Request (例如: /draw)" --> Routes
    Routes -- "2. 查詢 / 寫入資料" --> Models
    Models -- "3. 資料庫操作" --> DB
    DB -. "4. 回傳資料" .-> Models
    Models -. "5. 回傳物件/陣列" .-> Routes
    
    %% Response Flow
    Routes -- "6. 帶入資料渲染" --> Jinja
    Jinja -. "7. 生成 HTML" .-> Routes
    Routes -. "8. HTTP Response (HTML)" .-> Browser
```

---

## 4. 關鍵設計決策

1. **採用藍圖 (Blueprints) 切分路由**
   - **原因**：為了讓 `app.py` 保持極簡，我們會使用 Flask 的 Blueprint 功能，將「會員 (auth)」、「算命 (fortune)」、「香油錢 (payment)」的路由分開放置在 `app/routes/` 裡。這可以降低多人協作時的衝突，且讓程式碼邏輯更具可讀性。
2. **採用 SQLAlchemy 作為 ORM（物件關聯對映）**
   - **原因**：與其寫原生的 SQL 語法導致程式碼雜亂，我們決定引入 Flask-SQLAlchemy。這樣可以用 Python 的物件導向方式來操作 SQLite，對未來維護及程式碼的直覺性有巨大幫助。
3. **SSR 伺服器端渲染而非 API 導向**
   - **原因**：MVP 階段沒有複雜的前端互動需求，用 Jinja2 直接於後端渲染 HTML 回傳，可以最快速度實作出包含「算命、抽籤、登入」完整體驗的網站，同時對網頁的 SEO 較為友善。
4. **香油錢模組化隔離**
   - **原因**：考量到「捐香油錢」未來可能從模擬金流升級至真實第三方支付（如綠界），我們在架構上將其獨立為 `payment.py` 路由。在切換時只需修改這部分邏輯，不會影響到主要算命功能。

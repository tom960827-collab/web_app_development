# 系統路由與頁面設計 (Routes Design)

這份文件基於 PRD、FLOWCHART 與 ARCHITECTURE 規劃了所有的 Flask 路由、HTTP 方法以及對應的 Jinja2 模板。我們採用 Blueprint 機制將路由拆分為 `main`, `auth`, `fortune`, 和 `payment`。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁** | GET | `/` | `index.html` | 網站進入點，顯示介紹。 |
| **註冊頁面** | GET | `/auth/register` | `auth/register.html` | 顯示註冊表單。 |
| **處理註冊** | POST | `/auth/register` | — | 接收表單並建立新帳號，成功後重導向至登入頁。 |
| **登入頁面** | GET | `/auth/login` | `auth/login.html` | 顯示登入表單。 |
| **處理登入** | POST | `/auth/login` | — | 驗證帳號密碼，成功後重導向至首頁或個人主頁。 |
| **登出** | GET | `/auth/logout` | — | 清除 Session 狀態，重導向至首頁。 |
| **個人主頁** | GET | `/profile` | `user/profile.html` | 顯示個人資料與抽籤、香油錢紀錄。 |
| **抽籤頁面** | GET | `/fortune/draw` | `fortune/draw.html` | 顯示開始抽籤或觀看運勢的選擇頁。 |
| **處理抽籤** | POST | `/fortune/draw` | — | 隨機抽取一支籤，紀錄至 DB (若已登入)，重導向至結果頁。 |
| **籤詩結果** | GET | `/fortune/result/<id>`| `fortune/result.html`| 顯示抽籤結果（依據紀錄 ID 或籤詩 ID）。 |
| **捐贈頁面** | GET | `/payment/donate` | `payment/donate.html`| 顯示輸入捐獻金額與心意的表單。 |
| **模擬付款** | POST | `/payment/process` | — | 處理付款邏輯並紀錄至 DB，成功後重導向首頁。 |

## 2. 每個路由的詳細說明

### Main (首頁與個人主頁) - `app/routes/main.py`
- **`index` (`GET /`)**
  - 輸入：無
  - 處理邏輯：準備宣傳文案與入口連結。
  - 輸出：渲染 `index.html`。
- **`profile` (`GET /profile`)**
  - 輸入：需驗證登入狀態 Session。
  - 處理邏輯：查詢 `User` 取得基本資料，查詢 `FortuneRecord` 與 `Donation` 取得歷史供展示。
  - 輸出：渲染 `user/profile.html`。若未登入，重導向至 `/auth/login` 並顯示 401。

### Auth (會員) - `app/routes/auth.py`
- **`register` (`GET, POST /auth/register`)**
  - 輸入：表單欄位 `username`、`password`。
  - 處理邏輯：若是 POST，檢查使用者是否已存在，若否，雜湊密碼後存入 DB。
  - 輸出：成功重導至 `/auth/login`，失敗在原畫面顯示錯誤。
- **`login` (`GET, POST /auth/login`)**
  - 輸入：表單欄位 `username`、`password`。
  - 處理邏輯：若是 POST，驗證雜湊密碼，設定 User Session。
  - 輸出：成功重導至 `/profile` 或 `/`，失敗則在原本畫面顯示錯誤訊息。
- **`logout` (`GET /auth/logout`)**
  - 處理邏輯：清除 Session。
  - 輸出：重導向至 `/`。

### Fortune (算命) - `app/routes/fortune.py`
- **`draw` (`GET, POST /fortune/draw`)**
  - 輸入：表單或選項 (`category` 如觀音靈籤等)。
  - 處理邏輯：若是 POST，呼叫 Model 隨機抽選資料，若使用者已登入則存入 `FortuneRecord`。
  - 輸出：重導向至 `/fortune/result/<record_id_or_fortune_id>`。
- **`result` (`GET /fortune/result/<id>`)**
  - 輸入：URL 參數 `id`。
  - 處理邏輯：依據 ID 查出籤詩資料（與備註解籤紀錄）。
  - 輸出：渲染 `fortune/result.html` 給使用者看結果。如果 ID 不存在則回傳 404。

### Payment (香油錢) - `app/routes/payment.py`
- **`donate` (`GET /payment/donate`)**
  - 輸入：無。
  - 處理邏輯：準備表單頁面。如果為登入狀態可自動代入資料。
  - 輸出：渲染 `payment/donate.html`。
- **`process` (`POST /payment/process`)**
  - 輸入：表單欄位 `amount`、`message`。
  - 處理邏輯：呼叫 `Donation.create(...)` 並將 status 設定為 success（MVP 模擬付款成功）。
  - 輸出：重導向至首頁（建立 Flash message "感謝您的熱心捐款"）。

## 3. Jinja2 模板清單

所有模板皆繼承自 `base.html`，以共用頁首及頁尾。

- `base.html`：包含整體 `<html>` 結構，Navbar、Flash Message 區塊與 Footer。
- `index.html` (繼承 base)：大大的系統 Logo 與開始抽籤的超連結入囗。
- `auth/register.html` (繼承 base)：註冊表單。
- `auth/login.html` (繼承 base)：登入表單。
- `user/profile.html` (繼承 base)：會員主頁（抽籤歷史列表 + 香油錢明細）。
- `fortune/draw.html` (繼承 base)：準備抽籤引導與求籤按鈕。
- `fortune/result.html` (繼承 base)：籤詩單頁（內文、解白與社群分享。
- `payment/donate.html` (繼承 base)：香油錢捐獻表單。

## 4. 路由骨架程式碼
請參考 `app/routes/` 下的 `main.py`, `auth.py`, `fortune.py`, `payment.py` 等模組。

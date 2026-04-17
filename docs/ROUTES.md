# 路由設計文件 (ROUTES) - 線上算命系統

根據功能需求與架構設計，以下為前後端互動的 Flask 路由規劃。

## 1. 路由總覽表格

| 功能區塊 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :------- | :-------- | :------- | :------- | :--- |
| **首頁** | GET | `/` | `index.html` | 顯示系統介紹、主要功能入口 |
| **註冊頁面** | GET | `/auth/register` | `auth/register.html` | 呈現註冊表單 |
| **註冊操作** | POST | `/auth/register` | — | 接收資料、驗證、寫入資料庫後重導向至登入頁 |
| **登入頁面** | GET | `/auth/login` | `auth/login.html` | 呈現登入表單 |
| **登入操作** | POST | `/auth/login` | — | 驗證帳號密碼、建立 Session 後重導向至會員專區 |
| **登出操作** | GET | `/auth/logout` | — | 清除 Session 並重導向至首頁 |
| **測算大廳** | GET | `/divination` | `divination/index.html` | 顯示所有可用的測算項目 (線上求籤) |
| **求籤頁面** | GET | `/divination/draw` | `divination/draw.html` | 顯示求籤與搖籤筒的動畫互動畫面 |
| **抽籤與結果** | POST | `/divination/result` | `divination/result.html` | 執行抽籤演算法、儲存紀錄(若已登入)並顯示詳解 |
| **會員專區** | GET | `/profile` | `profile/index.html` | 顯示會員的基本資料、歷史占卜紀錄與香油錢紀錄 |
| **捐獻表單** | GET | `/donation` | `donation/index.html` | 顯示香油錢與祈福表單頁面 |
| **更新付款** | POST | `/donation/pay` | — | 接收模擬付款，更新狀態後重導向至會員專區 |

## 2. 每個路由的詳細說明

### `main` 模組 (首頁)
- **`GET /`**
  - **輸入**: 無
  - **處理邏輯**: 簡單回傳頁面。
  - **輸出**: 渲染 `index.html`。

### `auth` 模組 (會員身分驗證)
- **`GET /auth/register`**
  - **輸入**: 無
  - **輸出**: 渲染 `auth/register.html`。
- **`POST /auth/register`**
  - **輸入**: 表單提交的 `email`, `password`, `username`。
  - **處理邏輯**: 檢查必填，對密碼做雜湊加密，呼叫 user model 新增。如果 email 已存在則回報錯誤。
  - **輸出**: 成功則 flash 提示並導向 `/auth/login`；驗證失敗則 flash 錯誤並回傳 `auth/register.html`。
- **`GET /auth/login`**
  - **輸入**: 無
  - **輸出**: 渲染 `auth/login.html`。
- **`POST /auth/login`**
  - **輸入**: 表單提交的 `email`, `password`。
  - **處理邏輯**: 查詢此 email 使用者，比對密碼。正確則寫入 `session['user_id']`。
  - **輸出**: 成功重導向至 `/profile`；失敗回傳 `auth/login.html` 並顯示錯誤訊息。
- **`GET /auth/logout`**
  - **輸入**: 無
  - **處理邏輯**: 清除 `session`。
  - **輸出**: 重導向至 `/`。

### `divination` 模組 (測算服務)
- **`GET /divination`**
  - **輸入**: 無
  - **處理邏輯**: (可準備題庫類型或簡介文字)
  - **輸出**: 渲染 `divination/index.html`。
- **`GET /divination/draw`**
  - **輸入**: 無
  - **輸出**: 渲染 `divination/draw.html` (前端動畫互動)。
- **`POST /divination/result`**
  - **輸入**: 無特定輸入，或指定抽籤類別。
  - **處理邏輯**: 按隨機邏輯或從 poem model 亂數抽出 `id`。若使用者已登入，將其 `user_id` 與這張 `poem_id` 存入 record。
  - **輸出**: 渲染結果頁面 `divination/result.html`，丟入詩籤的 `content` 與 `explanation`。

### `profile` 模組 (會員專區)
- **`GET /profile`**
  - **輸入**: Session 中的 `user_id`。
  - **處理邏輯**: 確認是否已登入（若未登入則重導向 login）。透過 `user_id` 分別向 db 撈取會員狀態、歷史占卜、歷史捐獻紀錄。
  - **輸出**: 渲染 `profile/index.html`。

### `donation` 模組 (香油錢服務)
- **`GET /donation`**
  - **輸入**: 無
  - **輸出**: 渲染 `donation/index.html`。
- **`POST /donation/pay`**
  - **輸入**: 表單的 `amount` 與潛在付款資料。
  - **處理邏輯**: 模擬結帳，呼叫 donation model 寫入一筆成功付款的 log，綁定或不綁定 user_id (依是否登入而定)。
  - **輸出**: Flash 感謝通知，並重導向至 `/profile`。

## 3. Jinja2 模板清單

所有的視圖放置於 `app/templates/`。

- `base.html`：母版，包含 Navbar 以及 Flash Message。
- `index.html`：繼承自 base.html 的網站進入首頁。
- `auth/register.html`：包含註冊表單介面。
- `auth/login.html`：包含登入表單介面。
- `divination/index.html`：介紹各種測算的靜態頁區塊。
- `divination/draw.html`：操作抽籤流程的互動頁。
- `divination/result.html`：呈現詩籤文字、吉凶及詳解的觀看頁面。
- `profile/index.html`：分成左右或上下區塊，使用 for 迴圈列出該帳號的清單資料。
- `donation/index.html`：填選結緣金與寄託祈福內容的表單頁面。

## 4. 路由骨架程式碼
各獨立模組已依照 Blueprint 建立在 `app/routes/` 之下，實作邏輯留空待補：
- `main_routes.py`
- `auth_routes.py`
- `divination_routes.py`
- `profile_routes.py`
- `donation_routes.py`

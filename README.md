# ptt_gossip_bot

## 八卦版爆文機器人
#### Note: 僅測試用，並沒有特別調適 Prompt
1. 從八卦版撈取今日爆文
2. 利用 ChatGPT 總結重點
3. 發送至 Telegram 頻道


## 立即開始
1. clone 專案
2. 安裝套件
```
pip install -r requirements.txt
```
3. 新增 .env 檔案，複製以下內容，並將以下括號內的 KEY 改為自己的 KEY
```
OPEN_API_KEY={YOUR_OPEN_API_KEY}
TELEGRAM_BOT_TOKEN={YOUR_TELEGRAM_BOT_TOKEN}
TELEGRAM_CHAT_ID={YOUR_TELEGRAM_CHAT_ID}
```

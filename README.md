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
pip install -r requirement.txt
```
3. 修改 .env 檔案裡頭的 secret key
```
OPEN_API_KEY={YOUR_OPEN_API_KEY}
TELEGRAM_BOT_TOKEN={YOUR_TELEGRAM_BOT_TOKEN}
TELEGRAM_CHAT_ID={YOUR_TELEGRAM_CHAT_ID}
```

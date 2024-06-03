# QSticker Math Chatbot

---
``` Author
Made by Skyler Tsai in NTHU High Speed Network Lab directed by Prof. Nen-Fu, Huang
```
---

## 簡介
該模型為使用 OpenAI、LangChain、Chainlit 等函式庫實作出，建立於 QSticker 系統上的數學解題 / 生題聊天機器人。

---

## 設定

### 使用者設定
1. 點擊右上角的使用者後點選 Settings 進入使用者設定
2. 各項參數說明
    - `Expand Messages`: 是否自動展開過程
    - `Hide Chain of Thought`: 是否隱藏思維鍊步驟
    - `Dark Mode`: 是否開啟夜間模式

### 聊天機器人設定
1. 點擊訊息輸入欄位左側最靠右的 icon 進入聊天機器人設定
2. 各項參數說明
    - `OpenAI Chat Model`: 選擇要使用的 GPT 模型版本
        - `gpt-3.5-turbo-0125`
        - `gpt-4-1106-preview`
    - `Temperature for Question Generation`: GPT 的**溫度**值，值越大聲成的結過會越具隨機性及創造性；反之越小則越保守、穩定。
    - `Respond Language`: 選擇聊天機器人回覆用的語言
        - `zh-TW`: 繁體中文
        - `en`: 英文
    - `Enable human intervention`: 使否要求使用者驗證解題 / 生題結果是否正確，否則直接使用模型自我驗證的結果

---

## 使用流程
待補
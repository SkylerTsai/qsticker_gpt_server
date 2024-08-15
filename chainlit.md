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
1. 使用者登入，調整環境設定
2. 手動輸入題目 (簡答題、選擇題)，或自動從 QSticker 加入題目
3. `GPT math solver` 接收包含題目的提示
4. `GPT math solver` 根據提示選擇要用的工具 (wiki、Calculator、CoT、SymPy)
5. 回傳結果給 `GPT math solver` ，若知道答案則到第 6 步，反之回第 4 步
6. 將答案及過程結合題目翻譯成使用者的語言後回傳
7. 詢問使用者答案是否正確，是則到第 8 步，反之回第 3 步
8. 詢問使用者是否依據前面的題目及解答生成新題目，否則回第 2 步
9. `GPT generator` 接收包含題目、答案、過程的提示生成新題目
10. 將新題目結合提示傳給解題的 `GPT math solver`
11. `GPT math solver` 重複步驟 4、5，最後回傳新題目的解答及過程
12. 將新問題、解答、過程結合提示傳給 `GPT evaluator`
13. `GPT evaluator` 判斷題目、解答、過程是否合理後回傳
14. 答案不合理則回步驟 9，否則翻譯成使用者的語言後回傳
15. 詢問使用者新題目是否正確，是則到第 16 步，反之回第 9 步
16. 自動或手動將題目加入 QSticker 題組，回到第 2 步

## Link 
[QSticker Math Chatbot 簡介投影片](https://docs.google.com/presentation/d/1yA02drxiYYjDACRUUBDsdTj0GHRery-g/edit?usp=sharing&ouid=102630426525934980770&rtpof=true&sd=true)
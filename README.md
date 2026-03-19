# mark2win-bot

Telegram Bot for task management.

## Telegram Bot Setup

1. Deploy to Render.com
2. Set webhook
3. Send /register to bot

---
## Python ASR Client - 中文語音辨識客戶端

## 功能說明

將 C# ASR 程式轉換為 Python 版本，並新增麥克風即時錄音功能：

1. **即時麥克風錄音** - 取得麥克風聲音
2. **靜音偵測** - 偵測說話停止（預設 2 秒無聲）
3. **自動辨識** - 靜音觸發後自動上傳 ASR 服務
4. **結果儲存** - 辨識結果寫入文字檔

## 安裝

### 1. 安裝 Python 依賴

```bash
cd c:\data\OhMyOpenCode\sourceCode\CH_ASR\python_asr
pip install -r requirements.txt
```

### 2. 安裝 PyAudio（麥克風驅動）

**Windows:**
```bash
pip install pyaudio
```

如果安裝失敗，需要安裝 Microsoft C++ Build Tools，或嘗試：
```bash
pip install pipwin
pipwin install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux:**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

## 使用方式

### 基本用法（單次辨識）

```bash
python ch_asr.py <ASR_URL> <domain> [選項]
```

### 參數說明

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `url` | ASR 服務器 URL | (必填) |
| `domain` | ASR Domain | (必填) |
| `-s, --silence` | 靜音觸發秒數 | 2.0 秒 |
| `-o, --output` | 輸出結果檔案 | result.txt |
| `-c, --continuous` | 持續模式 | 單次 |

### 範例

**基本測試（使用預設值）：**
```bash
python ch_asr.py http://210.71.218.19:8086 whisper2_8k
```

**自訂靜音時間（3 秒）：**
```bash
python ch_asr.py http://210.71.218.19:8086 whisper2_8k -s 3
```

**指定輸出檔案：**
```bash
python ch_asr.py http://210.71.218.19:8086 whisper2_8k -o output.txt
```

**持續模式（辨識完繼續等待）：**
```bash
python ch_asr.py http://210.71.218.19:8086 whisper2_8k -c
```

## 使用流程

1. 執行上述命令
2. 出現「請說話」提示後，對著麥克風說話
3. 說完後等待 2 秒（可設定）靜音
4. 程式會自動上傳音頻到 ASR 服務器
5. 辨識結果顯示並儲存至 `result.txt`
6. 若為持續模式，會繼續監聽下一輪

## 持續模式說明

使用 `-c` 或 `--continuous` 參數進入持續模式：
- 辨識完成後自動繼續監聽
- 適合需要多次辨識的場景
- 按 `Ctrl+C` 中斷

## 測試腳本

```bash
# Windows
run_test.cmd
```

或直接執行：
```bash
cd c:\data\OhMyOpenCode\sourceCode\CH_ASR\python_asr
python ch_asr.py http://210.71.218.19:8086 whisper2_8k
```

## 參數對照表

| C# 參數 | Python 參數 |
|---------|-------------|
| args[0] (URL) | 第一個位置參數 |
| args[1] (domain) | 第二個位置參數 |
| args[2] (檔案) | 移除（改為麥克風錄音） |

## 疑難排解

### 1. 找不到 pyaudio
```bash
# Windows 安裝預編譯版本
pipwin install pyaudio
```

### 2. 麥克風無法使用
- 確認麥克風已連接並啟用
- 檢查系統隱私設定允許應用程式存取麥克風

### 3. ASR 連線失敗
- 確認 URL 和 domain 正確
- 檢查網路連線
- 確認 ASR 服務器是否正常運作

### 4. 辨識結果為空
- 檢查音頻是否正常錄製
- 嘗試調整靜音閾值（修改程式中的 threshold=500）

## 程式架構

```
ch_asr.py
├── AudioRecorder       # 麥克風錄音
├── SilenceDetector    # 靜音偵測
├── ASRClient          # ASR API 上傳
└── main()             # 主程式
```

## 程式碼特點

- 對應 C# 原始程式的 ASR 上傳邏輯
- 每次上傳 4800 bytes（與 C# 一致）
- 模擬 150ms 延遲（與 C# simTimeDelay 一致）
- 支援 NoInputTimeout 和 SpeechInCompleteTimeout

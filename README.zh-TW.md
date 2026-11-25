<div align="center">

# 🧰 gitignore-kit

**智慧型 .gitignore 產生與校驗工具** —— 讓每個儲存庫的忽略規則都正確、完整、可校驗

[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md)

![Version](https://img.shields.io/badge/version-1.0.0-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Python](https://img.shields.io/badge/python-3.8%2B-orange) ![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen)

</div>

## 🎉 介紹

寫程式時最惱人的細節之一：`.gitignore` 若是沒寫或寫得不完整，`node_modules`、`__pycache__`、建置產物就會被誤提交進儲存庫，歷史紀錄裡堆滿垃圾檔案，事後清理還得執行 `git rm --cached`。

**gitignore-kit** 用一條指令解決三件事：

1. **自動探測**專案技術堆疊（Python / Node / Go / Rust / Java…），產生對應的 `.gitignore`；
2. **增量合併**：已有的 `.gitignore` 不會被覆蓋，只補齊缺失的分節；
3. **違規檢查**：找出「已被 git 追蹤、卻命中忽略規則」的問題檔案，防患於未然。

純 Python 標準函式庫實作，**零第三方依賴**，隨套件內建 23 個範本，完全離線可用。

## ✨ 特性

- 🚀 **零依賴**：僅使用 Python 標準函式庫，`pip install` 秒裝，無安全審計負擔
- 🔍 **技術堆疊自動探測**：23 種語言 / 框架 / IDE / 作業系統範本，依特徵檔案智慧組合
- 🧩 **無損合併**：追加範本不會破壞你手寫的規則，重複分節自動去重
- 🛡️ **違規檢查**：基於 `git ls-files` 掃描已追蹤檔案，命中忽略規則立即警示
- 📦 **完全離線**：範本隨套件散布，不請求任何外部 API
- 💻 **跨平台**：Linux / macOS / Windows 全平台可用，自動適配終端配色
- 🧪 **測試完備**：規則引擎、探測、合併、CLI 端到端全覆蓋

## 🚀 快速開始

```bash
# 安裝
pip install gitignore-kit

# 在專案根目錄一鍵產生 .gitignore
gikit init

# 檢查是否已有檔案被誤追蹤
gikit check
```

就這麼簡單 —— 兩條指令，還你的儲存庫一個乾淨的暫存區。

## 📖 使用指南

### 🔍 自動產生

```bash
gikit init          # 探測當前目錄技術堆疊並產生/合併 .gitignore
gikit init -f       # 強制覆蓋已有 .gitignore
gikit init -p ./my-project      # 指定專案目錄
gikit init -t python docker     # 手動指定範本，跳過探測
```

### ➕ 追加範本

```bash
gikit add latex terraform    # 向已有 .gitignore 追加分節（自動去重）
```

### 📋 範本管理

```bash
gikit list          # 列出全部 23 個內建範本
gikit show python   # 檢視某個範本的具體內容
```

### 🛡️ 違規檢查

```bash
gikit check
```

輸出範例：

```
⚠ 發現 2 個違規檔案（已追蹤但命中 .gitignore 規則）:
  - debug.log
  - __pycache__/core.cpython-311.pyc
建議執行: git rm --cached <檔案> 以取消追蹤後提交。
```

結束代碼：`0` 通過 / `1` 存在違規 —— 可直接接入 CI 或 pre-commit 鉤子。

### 🧩 程式介面

```python
from gitignore_kit import checker, scanner

stacks = scanner.scan(".")              # ['python', 'build', 'macos', ...]
violations = checker.find_violations(".")  # ['debug.log', ...]
```

## 💡 設計迭代

**v1.0.0（目前）**
- 核心：規則引擎（支援 `*`、`?`、`**`、`[...]`、否定規則、目錄規則、根錨定）
- 23 個內建範本 + 基於特徵檔案的技術堆疊探測
- `init` / `add` / `list` / `show` / `check` 五個子指令
- 跨平台 CI（Ubuntu / macOS / Windows × Python 3.8 / 3.12）

**規劃中**
- [ ] `check --fix`：自動執行 `git rm --cached` 並提示提交
- [ ] pre-commit 鉤子一鍵安裝
- [ ] 範本社群貢獻通道與版本化管理

## 📦 打包部署

```bash
# 從原始碼安裝
git clone https://github.com/gitstq/gitignore-kit.git
cd gitignore-kit
pip install .

# 執行測試
pytest tests/ -v

# 一鍵建置發布套件（sdist + wheel + SHA256 校驗和）
bash scripts/build.sh
```

Wheel 套件為通用建置，Windows / macOS / Linux 均可直接安裝，無需編譯。

## 🤝 貢獻

歡迎提交 Issue 與 Pull Request！新增範本、完善規則引擎、補充測試都非常有價值。請閱讀 [CONTRIBUTING.md](CONTRIBUTING.md) 了解規範。

## 📄 授權條款

本專案基於 [MIT License](LICENSE) 開源。

<div align="center">

# 🧰 gitignore-kit

**智能 .gitignore 生成与校验工具** —— 让每一个仓库的忽略规则都正确、完整、可校验

[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md)

![Version](https://img.shields.io/badge/version-1.0.0-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Python](https://img.shields.io/badge/python-3.8%2B-orange) ![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen)

</div>

## 🎉 介绍

写代码时最让人头疼的细节之一：`.gitignore` 要么没写、要么不全，结果 `node_modules`、`__pycache__`、构建产物被误提交进仓库，历史里堆满垃圾文件，事后清理还得 `git rm --cached`。

**gitignore-kit** 用一条命令解决三件事：

1. **自动探测**项目技术栈（Python / Node / Go / Rust / Java…），生成对应的 `.gitignore`；
2. **增量合并**：已有 `.gitignore` 不会被覆盖，只补齐缺失的分节；
3. **违规检查**：找出「已被 git 跟踪、却命中忽略规则」的问题文件，防患于未然。

纯 Python 标准库实现，**零第三方依赖**，随包内置 23 个模板，完全离线可用。

## ✨ 特性

- 🚀 **零依赖**：仅 Python 标准库，`pip install` 秒装，无安全审计负担
- 🔍 **技术栈自动探测**：23 种语言 / 框架 / IDE / 操作系统模板，按特征文件智能组合
- 🧩 **无损合并**：追加模板不会破坏你手写的规则，重复分节自动去重
- 🛡️ **违规检查**：基于 `git ls-files` 扫描已跟踪文件，命中忽略规则即刻告警
- 📦 **完全离线**：模板随包分发，不请求任何外部 API
- 💻 **跨平台**：Linux / macOS / Windows 全平台可用，自动适配终端配色
- 🧪 **测试完备**：规则引擎、探测、合并、CLI 端到端全覆盖

## 🚀 快速开始

```bash
# 安装
pip install gitignore-kit

# 在项目根目录一键生成 .gitignore
gikit init

# 检查是否已有文件被误跟踪
gikit check
```

就这么简单 —— 两条命令，还你的仓库一个干净的暂存区。

## 📖 使用指南

### 🔍 自动生成

```bash
gikit init          # 探测当前目录技术栈并生成/合并 .gitignore
gikit init -f       # 强制覆盖已有 .gitignore
gikit init -p ./my-project      # 指定项目目录
gikit init -t python docker     # 手动指定模板，跳过探测
```

### ➕ 追加模板

```bash
gikit add latex terraform    # 向已有 .gitignore 追加分节（自动去重）
```

### 📋 模板管理

```bash
gikit list          # 列出全部 23 个内置模板
gikit show python   # 查看某个模板的具体内容
```

### 🛡️ 违规检查

```bash
gikit check
```

输出示例：

```
⚠ 发现 2 个违规文件（已跟踪但命中 .gitignore 规则）:
  - debug.log
  - __pycache__/core.cpython-311.pyc
建议执行: git rm --cached <文件> 以取消跟踪后提交。
```

退出码：`0` 通过 / `1` 存在违规 —— 可直接接入 CI 或 pre-commit 钩子。

### 🧩 编程接口

```python
from gitignore_kit import checker, scanner

stacks = scanner.scan(".")              # ['python', 'build', 'macos', ...]
violations = checker.find_violations(".")  # ['debug.log', ...]
```

## 💡 设计迭代

**v1.0.0（当前）**
- 核心：规则引擎（支持 `*`、`?`、`**`、`[...]`、否定规则、目录规则、根锚定）
- 23 个内置模板 + 基于特征文件的技术栈探测
- `init` / `add` / `list` / `show` / `check` 五个子命令
- 跨平台 CI（Ubuntu / macOS / Windows × Python 3.8 / 3.12）

**规划中**
- [ ] `check --fix`：自动执行 `git rm --cached` 并提示提交
- [ ] pre-commit 钩子一键安装
- [ ] 模板社区贡献通道与版本化管理

## 📦 打包部署

```bash
# 从源码安装
git clone https://github.com/gitstq/gitignore-kit.git
cd gitignore-kit
pip install .

# 运行测试
pytest tests/ -v

# 一键构建发布包（sdist + wheel + SHA256 校验和）
bash scripts/build.sh
```

Wheel 包为通用构建，Windows / macOS / Linux 均可直接安装，无需编译。

## 🤝 贡献

欢迎提交 Issue 与 Pull Request！新增模板、完善规则引擎、补充测试都非常有价值。请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解规范。

## 📄 协议

本项目基于 [MIT License](LICENSE) 开源。

#!/usr/bin/env bash
# 一键打包脚本：构建 sdist + wheel，并生成 SHA256 校验和
set -euo pipefail
cd "$(dirname "$0")/.."

python3 -m build
cd dist
sha256sum *.tar.gz *.whl > SHA256SUMS.txt
cd ..
echo "构建完成："
ls -lh dist

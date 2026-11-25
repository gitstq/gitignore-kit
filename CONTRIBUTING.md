# 🤝 贡献指南

感谢关注 **gitignore-kit**！欢迎以任何形式参与贡献。

## 🐛 报告问题
- 使用 [Issue 模板](https://github.com/gitstq/gitignore-kit/issues/new) 描述复现步骤与期望行为；
- 附上 `gikit --version` 与操作系统信息。

## 💡 提交代码
1. Fork 仓库并创建特性分支：`git checkout -b feat/your-feature`；
2. 提交信息遵循 [Angular 规范](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#-git-commit-guidelines)：
   `feat` / `fix` / `docs` / `refactor` / `test` / `chore`；
3. 运行并确保全部测试通过：
   ```bash
   pytest tests/ -v
   ```
4. 新增模板请同步更新 `src/gitignore_kit/templates.py` 中的 `LABELS` 与测试；
5. 发起 Pull Request，说明改动动机与自测结果。

## 📦 新增模板规范
- 一个模板一个文件，存放于 `src/gitignore_kit/data/templates/<name>.gitignore`；
- 只保留该生态公认的模式，避免大而全；
- 如对应特定技术栈，请在 `scanner.py` 注册探测规则并补充单元测试。

## 📄 许可
提交即表示你同意代码以 [MIT](LICENSE) 协议开源。

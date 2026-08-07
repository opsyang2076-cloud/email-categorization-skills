# 贡献指南

感谢您对邮件分类器的兴趣！本文档提供了贡献的指南和说明。

## 🤝 如何贡献

### 报告错误

在创建错误报告之前，请检查现有问题。当您创建错误报告时，请包含尽可能多的细节：

1. **使用清晰的标题**
2. **描述问题** - 发生了什么 vs. 您期望什么
3. **复现步骤** - 编号步骤列表
4. **期望行为** - 应该发生什么
5. **实际行为** - 实际发生了什么
6. **截图** - 如果适用
7. **环境** - 操作系统、Python 版本、邮件提供商

### 建议功能

欢迎功能请求！请：

1. 先检查现有问题
2. 使用清晰标题
3. 描述功能及其用途
4. 提供使用示例
5. 提及任何实现想法

### 代码贡献

1. **Fork 仓库**
2. **从 `main` 创建分支**
3. **进行更改**
4. **为新功能添加测试**
5. **运行测试** 确保没有破坏
6. **提交拉取请求**

## 📋 开发设置

### 先决条件

- Python 3.8 或更高版本
- Git
- pip（Python 包管理器）

### 初始设置

```bash
# 克隆您的 fork
git clone https://github.com/YOUR_USERNAME/email-classifier.git
cd email-classifier

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 安装 pre-commit hooks（可选）
pre-commit install
```

### 运行测试

```bash
# 运行所有测试
python -m pytest tests/ -v

# 运行覆盖率测试
python -m pytest tests/ --cov=scripts --cov-report=html

# 运行特定测试
python -m pytest tests/test_email_classifier.py -v -k verification

# 运行 linter
flake8 scripts/ tests/

# 格式化代码
black scripts/ tests/
isort scripts/ tests/
```

## 🎨 代码风格

### Python 风格

- 遵循 [PEP 8](https://peps.python.org/pep-0008/) 风格指南
- 使用 [Black](https://black.readthedocs.io/) 进行格式化
- 使用 [isort](https://pycqa.github.io/isort/) 进行导入排序
- 使用 [flake8](https://flake8.pycqa.org/) 进行 linting
- 最大行长度：88 个字符（Black 默认）

### 文档风格

- 使用 [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- 记录所有公共函数和类
- 在有帮助时在 docstrings 中包含示例
- 保持 README.md 更新

### 提交信息

遵循 [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)：

```
feat: 添加验证码检测
fix: 解决 IMAP 连接超时
docs: 更新 Gmail 设置指南
test: 添加频率分析测试
refactor: 简化分类逻辑
chore: 更新依赖
```

类型：
- `feat`：新功能
- `fix`：错误修复
- `docs`：文档更改
- `test`：添加或更新测试
- `refactor`：既不修复错误也不添加功能代码更改
- `chore`：维护任务

## 🧪 测试指南

### 编写测试

1. **尽可能每个测试一个断言**
2. **使用描述性测试名称**：`test_verification_code_detection()`
3. **测试边界情况**：空输入、无效数据、边界值
4. **使用 fixtures** 进行通用设置
5. **模拟外部依赖**（IMAP、文件系统）

### 测试类别

```python
# 单元测试
def test_classification_logic():
    """测试核心分类算法。"""
    ...

# 集成测试
def test_email_fetch():
    """测试从 IMAP 服务器获取邮件。"""
    ...

# 边界情况测试
def test_empty_email_list():
    """测试处理空邮件列表。"""
    ...
```

### 测试覆盖率

目标是：
- 80%+ 代码覆盖率
- 所有新代码必须有测试
- 关键路径必须测试

## 📚 文档指南

### 更新文档

1. **README.md**：随新功能更新
2. **SKILL.md**：更新 Hermes Agent 集成文档
3. **references/**：根据需要添加新指南
4. **docs/**：添加详细文档

### 文档检查清单

- [ ] 代码示例准确
- [ ] 链接工作
- [ ] 截图当前
- [ ] 安装说明完整
- [ ] 故障排除部分更新

## 🔍 拉取请求流程

### 提交前

1. **更新文档**（如需要）
2. **为新功能添加测试**
3. **运行所有测试** 确保通过
4. **使用 black 和 isort 格式化代码**
5. **用 flake8 检查 linting**
6. **如果适用，更新 CHANGELOG**

### PR 模板

```markdown
## 描述
更改的简要描述

## 更改类型
- [ ] 错误修复
- [ ] 新功能
- [ ] 文档更新
- [ ] 重构
- [ ] 性能改进

## 测试
- [ ] 测试在本地通过
- [ ] 添加了新测试
- [ ] 覆盖了边界情况

## 检查清单
- [ ] 代码遵循风格指南
- [ ] 自我审查代码
- [ ] 在需要时添加注释
- [ ] 更新文档
```

## 🎯 需要帮助的领域

目前正在寻找贡献：

1. **ML 集成**：基于机器学习的分类
2. **更多邮件提供商**：Yahoo、iCloud 等
3. **Web 界面**：基于浏览器的配置
4. **移动应用**：iOS/Android 支持
5. **性能**：大型邮箱优化
6. **文档**：翻译、教程、视频

## 📞 获取帮助

- 💬 [GitHub 讨论](https://github.com/YOUR_USERNAME/email-classifier/discussions)
- 🐛 [问题追踪](https://github.com/YOUR_USERNAME/email-classifier/issues)
- 📧 邮箱：your.email@example.com

## 🏆 认可

贡献者将：
- 添加到 CONTRIBUTORS.md
- 在 release notes 中提到
- 在文档中 credit

## 📜 行为准则

### 我们的承诺

我们作为成员、贡献者和领导者承诺让参与我们的项目成为一个免于骚扰的体验。

### 标准

促进积极环境的行为示例：
- 使用欢迎和包容的语言
- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 专注于对社区最好的事情

### 执行

将不可接受的行为报告给项目维护者。

## 🎉 谢谢！

您的贡献让每个人都能更好地使用这个项目。感谢您帮助改进邮件分类器！

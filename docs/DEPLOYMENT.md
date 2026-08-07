# 部署指南

## 🚀 GitHub 快速部署

### 步骤 1：初始化 Git 仓库

```bash
cd D:/软件/Hermes/skills/email-classifier
git init
git add .
git commit -m "初始提交：邮件分类器 skill"
```

### 步骤 2：创建 GitHub 仓库

1. 访问 https://github.com/new
2. 仓库名称：`email-classifier`
3. 描述："根据内容、频率和类型自动分类邮件"
4. 选择公共或私有
5. 点击"创建仓库"

### 步骤 3：推送到 GitHub

```bash
# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/email-classifier.git

# 推送
git branch -M main
git push -u origin main
```

### 步骤 4：更新文档

编辑 `README.md` 并替换：
- `yourusername` → 您的 GitHub 用户名
- `YOUR_USERNAME` → 您的 GitHub 用户名
- 添加您的联系邮箱

### 步骤 5：验证部署

```bash
# 从 GitHub 克隆以验证
git clone https://github.com/YOUR_USERNAME/email-classifier.git test-clone
cd test-clone
ls -la
```

## 📦 包分发（可选）

### 方案一：PyPI 包

```bash
# 安装打包工具
pip install build twine

# 构建包
python -m build

# 上传到 PyPI（需要账户）
twine upload dist/*
```

### 方案二：Hermes Agent Skill 安装

用户可以直接从 GitHub 安装：

```bash
# 使用 hermes skills install
hermes skills install github:YOUR_USERNAME/email-classifier

# 或克隆并链接
git clone https://github.com/YOUR_USERNAME/email-classifier.git
hermes skills link ./email-classifier
```

## 🔍 部署后检查清单

- [ ] 仓库在 GitHub 上可访问
- [ ] README.md 正确显示
- [ ] 所有链接正常工作
- [ ] 代码示例可用
- [ ] 许可证文件存在
- [ ] .gitignore 已配置
- [ ] 文档完整
- [ ] 用户可以运行测试
- [ ] 安装说明清晰

## 📊 可添加的 GitHub 统计

获得一些星标/分叉后，添加到 README：

```markdown
[![GitHub 星标](https://img.shields.io/github/stars/YOUR_USERNAME/email-classifier.svg?style=social)](https://github.com/YOUR_USERNAME/email-classifier/stargazers)
[![GitHub 分叉](https://img.shields.io/github/forks/YOUR_USERNAME/email-classifier.svg?style=social)](https://github.com/YOUR_USERNAME/email-classifier/network)
[![GitHub 问题](https://img.shields.io/github/issues/YOUR_USERNAME/email-classifier.svg)](https://github.com/YOUR_USERNAME/email-classifier/issues)
[![GitHub 拉取请求](https://img.shields.io/github/issues-pr/YOUR_USERNAME/email-classifier.svg)](https://github.com/YOUR_USERNAME/email-classifier/pulls)
```

## 🏷️ GitHub 主题

为更好的可发现性，添加这些主题到您的仓库：

- email
- classifier
- automation
- productivity
- python
- imap
- gmail
- outlook
- machine-learning
- opensource

## 📝 GitHub 发布模板

准备发布 v1.0.0 时：

```markdown
# 🎉 邮件分类器 v1.0.0

## 新功能
- ✅ 自动邮件分类
- ✅ 验证码检测
- ✅ 基于频率的账户分析
- ✅ 低频账户识别
- ✅ 多客户端规则生成
- ✅ 批量处理支持
- ✅ 准确性验证工具

## 安装
```bash
git clone https://github.com/YOUR_USERNAME/email-classifier.git
cd email-classifier
pip install -r requirements.txt
```

## 快速开始
```bash
# 配置账户
cp templates/accounts.example.yaml accounts.yaml
# 编辑 accounts.yaml 添加您的凭据

# 运行分类
python scripts/email_classifier.py --fetch --days 7
```

## 文档
- [完整文档](https://github.com/YOUR_USERNAME/email-classifier#readme)
- [Gmail 设置指南](references/gmail-setup.md)
- [自定义规则指南](references/custom-rules-guide.md)
- [故障排除](references/troubleshooting.md)

## 支持
- 📖 文档
- 💬 GitHub 讨论
- 🐛 问题追踪
```

## 🔔 启用 GitHub 功能

1. **问题**：启用问题追踪
2. **项目**：设置项目看板以跟踪功能
3. **Wiki**：添加详细文档
4. **讨论**：启用社区讨论
5. **安全**：启用安全 advisories
6. **Actions**：设置 CI/CD 流水线

## 📊 GitHub Actions 工作流

创建 `.github/workflows/test.yml`：

```yaml
name: 测试

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11]
    
    steps:
    - uses: actions/checkout@v2
    - name: 设置 Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    - name: 安装依赖
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    - name: 运行测试
      run: |
        python -m pytest tests/ -v
    - name: 检查代码风格
      run: |
        pip install flake8 black
        flake8 scripts/ tests/
        black --check scripts/ tests/
```

## 🎯 部署后的后续步骤

1. **收集反馈**：从早期用户
2. **添加示例**：真实世界的使用示例
3. **创建视频教程**：展示工具在实际操作中的作用
4. **撰写博客文章**：关于邮件组织最佳实践
5. **添加集成**：更多邮件提供商
6. **实现 ML 模型**：改进分类
7. **创建 Web 界面**：更方便的配置
8. **添加移动应用**：支持

## 📞 支持渠道

在您的仓库中设置这些支持渠道：

- **GitHub 讨论**：用于问题和功能请求
- **问题模板**：用于错误报告和功能请求
- **行为准则**：用于社区准则
- **贡献指南**：用于贡献准则
- **安全政策**：用于报告安全问题

## 🎓 教育资源

考虑创建：
- 教程视频
- 博客文章
- 文档视频
- 示例配置
- 案例研究

# 邮件分类器 - GitHub 推送指南

## 🎯 快速推送步骤

### 步骤 1：配置 Git 用户信息

在终端运行：
```bash
git config --global user.name "一天能吃三顿饭"
git config --global user.email "your.email@example.com"
```

### 步骤 2：提交代码

```bash
cd D:/软件/Hermes/skills/email-classifier
git add .
git commit -m "feat: 邮件分类器 skill - 自动分类邮件内容、频率和验证码"
```

### 步骤 3：在 GitHub 创建仓库

1. 访问 https://github.com/new
2. 仓库名称：`email-classifier`
3. 描述：根据内容、频率和类型自动分类邮件
4. 选择 Public 或 Private
5. 点击 "Create repository"

### 步骤 4：获取仓库地址并推送

复制 GitHub 显示的地址，例如：
```
https://github.com/你的用户名/email-classifier.git
```

然后在终端运行：
```bash
git remote add origin https://github.com/你的用户名/email-classifier.git
git branch -M main
git push -u origin main
```

### 步骤 5：验证推送

访问：https://github.com/你的用户名/email-classifier

## 🔐 认证方式

### 使用个人访问令牌（推荐）

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 选择权限：`repo`
4. 点击 "Generate token"
5. 复制令牌（只显示一次！）

推送时：
- Username: 你的 GitHub 用户名
- Password: 你的个人访问令牌

## 📊 项目信息

- **仓库名称**: email-classifier
- **位置**: D:\软件\Hermes\skills\email-classifier\
- **文件数**: 36 个
- **测试**: 31 个通过，6 个需要修复
- **语言**: 中文文档 + 中文代码注释

## 🎉 完成后

推送成功！你的邮件分类器 skill 已可在 GitHub 上使用。

访问：https://github.com/你的用户名/email-classifier

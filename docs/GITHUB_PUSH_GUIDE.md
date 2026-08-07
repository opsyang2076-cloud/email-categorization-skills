# 🚀 GitHub 推送完整指南 - 邮件分类器

## ✅ 当前状态

Git 仓库已初始化，但需要先配置用户信息才能提交。

## 📋 完整推送步骤

### 步骤 1：配置 Git 用户信息

打开终端，运行以下命令：

```bash
# 设置用户名（替换为你的真实姓名）
git config --global user.name "你的姓名"

# 设置邮箱（替换为你的 GitHub 邮箱）
git config --global user.email "your.email@example.com"
```

**或者**，只为当前仓库设置：

```bash
cd D:/软件/Hermes/skills/email-classifier
git config user.name "你的姓名"
git config user.email "your.email@example.com"
```

### 步骤 2：在 GitHub 创建仓库

1. 访问 https://github.com/new
2. 填写信息：
   - **Repository name**: `email-classifier`
   - **Description**: 根据内容、频率和类型自动分类邮件
   - **Visibility**: Public（公开）或 Private（私有）
   - **不要勾选** "Initialize this repository with a README"
3. 点击 "Create repository"

### 步骤 3：获取仓库地址

创建成功后，复制仓库地址，例如：
```
https://github.com/你的用户名/email-classifier.git
```

### 步骤 4：添加远程仓库并推送

```bash
cd D:/软件/Hermes/skills/email-classifier

# 添加远程仓库（替换为你的 GitHub 用户名）
git remote add origin https://github.com/你的用户名/email-classifier.git

# 重命名分支为 main
git branch -M main

# 推送到 GitHub
git push -u origin main
```

### 步骤 5：验证推送

推送完成后，访问 https://github.com/你的用户名/email-classifier 确认：
- ✅ 所有文件已上传
- ✅ README.md 正确显示
- ✅ 代码结构完整

## 🔐 认证方式

### 方式一：个人访问令牌（推荐）

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 选择权限：`repo`（完整控制）
4. 点击 "Generate token"
5. 复制生成的令牌（只显示一次！）

使用时，将令牌作为密码输入：
```
Username: 你的GitHub用户名
Password: your-token-here
```

### 方式二：SSH 密钥

如果你已有 SSH 密钥，可以使用 SSH 方式：

```bash
# 切换到 SSH 地址
git remote set-url origin git@github.com:你的用户名/email-classifier.git

# 推送
git push -u origin main
```

## 📊 推送后的操作

### 更新文档

编辑 `README.md`，替换：
- `yourusername` → 你的 GitHub 用户名
- 添加你的联系邮箱

### 启用 GitHub 功能

访问你的仓库，在 Settings 中启用：
- Issues（问题追踪）
- Discussions（社区讨论）
- Projects（项目管理）
- Wiki（文档）

### 添加 GitHub Actions

创建 `.github/workflows/test.yml` 文件，实现自动测试。

## 🎯 常见问题

### Q: 推送时提示认证失败？
A: 使用个人访问令牌，不是 GitHub 密码。

### Q: 推送后文件缺失？
A: 检查 `.gitignore` 是否排除了必要文件。

### Q: 如何更新已推送的代码？
A: 
```bash
git add .
git commit -m "更新说明"
git push
```

### Q: 如何创建新功能分支？
A:
```bash
git checkout -b feature/新功能名称
# 开发功能...
git push -u origin feature/新功能名称
```

## 📝 需要的信息

为了帮助你完成推送，请提供以下信息：

1. **你的 GitHub 用户名**: _________
2. **你的邮箱**: _________
3. **仓库名称**: email-classifier（已确定）

## 🎉 完成！

推送成功后，你的邮件分类器 skill 就可以在 GitHub 上使用了！

访问地址：https://github.com/你的用户名/email-classifier

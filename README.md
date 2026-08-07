# 邮件分类器 - GitHub README

<p align="center">
  <img src="docs/images/logo.png" alt="邮件分类器 Logo" width="200">
</p>

<h1 align="center">邮件分类器</h1>

<p align="center">
  <strong>根据内容、频率和类型自动分类邮件</strong>
</p>

<p align="center">
  <a href="https://github.com/yitian-neng-sanfan/email-classifier/actions">
    <img src="https://github.com/yitian-neng-sanfan/email-classifier/workflows/Test/badge.svg" alt="测试">
  </a>
  <a href="https://github.com/yitian-neng-sanfan/email-classifier/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="许可证">
  </a>
  <a href="https://python.org">
    <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python">
  </a>
  <a href="https://github.com/yitian-neng-sanfan/email-classifier/stargazers">
    <img src="https://img.shields.io/github/stars/yitian-neng-sanfan/email-classifier.svg?style=social" alt="星标">
  </a>
</p>

## ✨ 功能特性

### 🎯 智能邮件分类
- **8+ 预定义类别**：验证码、社交、促销、工作、个人、通知、交易、论坛
- **基于模式的检测**：使用关键词、发件人模式和主题行分析
- **可配置的置信度阈值**：根据您的需求调整灵敏度

### 🔐 验证码检测
- 自动识别 OTP、密码重置和 2FA 验证码
- 常见验证码格式的模式匹配（4-8 位数字）
- 将验证码邮件与常规邮件分离

### 📊 频率分析
- 分析跨账户的邮件参与模式
- 按频率分类账户：daily_high、daily_medium、daily_low、weekly_sporadic
- 识别需要关注的低频账户

### 🏷️ 多客户端支持
- **Gmail**：生成标签和过滤器
- **Outlook**：创建规则和 VBA 脚本
- **IMAP**：服务器端过滤规则
- **CSV 导出**：导入任何邮件客户端

### ⚡ 批量处理
- 同时处理多个电子邮件账户
- 针对大型邮箱优化性能
- 可配置的批量大小和缓存

### 🧪 准确性验证
- 将自动分类与手动标签进行比较
- 计算精确率、召回率和 F1 分数
- 生成改进建议

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/yitian-neng-sanfan/email-classifier.git
cd email-classifier

# 安装依赖
pip install -r requirements.txt
```

### 基本使用

```bash
# 1. 配置您的电子邮件账户
cp templates/accounts.example.yaml accounts.yaml
# 编辑 accounts.yaml 添加您的凭据

# 2. 测试连接
python scripts/email_classifier.py --test-connection

# 3. 获取并分类邮件
python scripts/email_classifier.py --fetch --days 7 --output results.json

# 4. 分析频率模式
python scripts/frequency_analyzer.py --input results.json --output frequency_report.json

# 5. 生成分类规则
python scripts/rule_generator.py --input results.json --format gmail-labels
```

### 示例输出

```
============================================================
分类摘要
============================================================
处理的邮件总数：1,250
分析的账户数：3

类别分布：
  verification_codes: 45 封邮件
  work: 320 封邮件
  promotions: 180 封邮件
  social: 95 封邮件
  notifications: 78 封邮件
  transactions: 52 封邮件
  forums: 35 封邮件
  personal: 445 封邮件

检测到的高频账户：1
  - old-forum@example.com（每天 0.3 封邮件）
    建议：考虑归档或取消订阅
============================================================
```

## 📚 文档

- [📖 完整文档](docs/)
- [📧 Gmail 设置指南](references/gmail-setup.md)
- [📧 Outlook 设置指南](references/outlook-setup.md)
- [🦞 飞书/Lark 集成](references/lark-mail-integration.md)
- [🎨 自定义规则指南](references/custom-rules-guide.md)
- [🔧 故障排除](references/troubleshooting.md)
- [📊 API 参考](docs/api-reference.md)

## 🏗️ 架构

```
┌─────────────────────────────────────────────────────────────┐
│                    邮件分类器                                │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   获取器    │  │  分类器     │  │  分析器     │        │
│  │  (IMAP)     │  │  (规则/ML)  │  │  (频率)     │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
│         │                │                 │               │
│         └────────────────┼─────────────────┘               │
│                          │                                 │
│                  ┌───────▼───────┐                         │
│                  │   报告生成    │                         │
│                  │  (规则/导出)  │                         │
│                  └───────┬───────┘                         │
└──────────────────────────┼─────────────────────────────────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
        ┌─────▼────┐ ┌────▼────┐ ┌────▼────┐
        │ Gmail    │ │Outlook  │ │ IMAP    │
        │ 标签     │ │ 规则    │ │ 过滤器  │
        └──────────┘ └─────────┘ └─────────┘
```

## 📊 支持的类别

| 类别 | 描述 | 检测模式 |
|------|------|----------|
| **verification_codes** | OTP、密码重置 | 数字代码、安全关键词 |
| **social** | 社交媒体通知 | 平台特定发件人 |
| **promotions** | 营销邮件 | 优惠/折扣关键词 |
| **work** | 专业通信 | 商业域名 |
| **personal** | 个人通信 | 非正式模式 |
| **notifications** | 系统警报 | 安全/更新关键词 |
| **transactions** | 收据、发票 | 支付关键词 |
| **forums** | 社区讨论 | 论坛平台发件人 |

## 🔧 配置

### 账户配置（accounts.yaml）

```yaml
accounts:
  - name: "工作"
    provider: "gmail"
    email: "your.work@gmail.com"
    imap_host: "imap.gmail.com"
    imap_port: 993
    auth_type: "app_password"
    password: "your-app-password"  # 使用应用密码，不是普通密码
```

### 自定义规则（custom_rules.yaml）

```yaml
custom_categories:
  - name: "重要客户"
    keywords: ["发票", "合同", "法律"]
    sender_domains: ["client1.com", "client2.com"]
    weight: 1.5
    action:
      label: "重要/客户"
      priority: "高"
```

## 🧪 测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行覆盖率测试
pytest tests/ --cov=scripts --cov-report=html

# 运行特定测试
pytest tests/test_email_classifier.py -v -k verification
```

## 🔒 安全

- ✅ 所有处理都在本地进行 - 不发送数据到外部服务器
- ✅ 使用应用密码，不是普通密码
- ✅ 凭据永远不会提交到 git（见 `.gitignore`）
- ✅ 生成的规则在应用前会经过审查
- ✅ 支持 OAuth 认证（推荐生产环境使用）

## 🤝 贡献

欢迎贡献！提交 PR 前请阅读我们的[贡献指南](docs/CONTRIBUTING.md)。

### 开发设置

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装开发依赖
pip install -r requirements-dev.txt

# 提交前运行测试
pytest tests/ -v
```

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- [Hermes Agent](https://github.com/NousResearch/hermes-agent) - Skill 框架集成
- 邮件提供商（Gmail、Outlook、IMAP）- 邮件访问 API
- 开源分类库 - 模式匹配和机器学习

## 📞 支持

- 📖 [文档](docs/)
- 💬 [讨论](https://github.com/yitian-neng-sanfan/email-classifier/discussions)
- 🐛 [问题追踪](https://github.com/yitian-neng-sanfan/email-classifier/issues)
- 📧 邮箱：yitian-neng-sanfan@example.com

## 🌟 Star 历史

[![Star History Chart](https://api.star-history.com/svg?repos=yitian-neng-sanfan/email-classifier&type=Date)](https://star-history.com/#yitian-neng-sanfan/email-classifier&Date)

---

**注意**：此技能设计用于与 Hermes Agent 的 skill 系统一起使用，但也可以独立使用。对于飞书/Lark 集成，请使用 `lark-mail` skill。

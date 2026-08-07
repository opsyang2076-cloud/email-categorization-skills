# 邮件分类器 Skill

一个全面的邮件分类系统，根据内容、发件人模式和参与频率自动将邮件分类。

## 🎯 核心功能

### 1. **自动邮件分类**
- 将邮件分类到 8+ 个智能类别
- 使用模式匹配、关键词分析和发件人启发式规则
- 高准确性，可配置的置信度阈值

### 2. **验证码检测**
- 自动识别 OTP、密码重置和 2FA 验证码
- 将验证码邮件与常规通信分离
- 常见代码格式的模式匹配（4-8 位数字）

### 3. **基于频率的账户分析**
- 分析跨账户的邮件参与模式
- 将账户分类为：daily_high、daily_medium、daily_low、weekly_sporadic
- 识别需要关注的低频账户

### 4. **低频账户检测**
- 标记活动极少的账户（<1 封邮件/天）
- 提供可行的建议（归档、取消订阅等）
- 跟踪时间趋势

### 5. **多客户端规则生成**
- 自动为 Gmail、Outlook 和 IMAP 生成过滤器
- 导出到 CSV、YAML 或原生客户端格式
- 一键应用规则

### 6. **批量处理**
- 同时处理多个电子邮件账户
- 集中配置和报告
- 针对大型邮箱优化性能

### 7. **准确性验证**
- 将自动分类与手动标签进行比较
- 计算精确率、召回率和 F1 分数
- 生成改进建议

## 📦 快速开始

```bash
# 1. 安装
git clone https://github.com/yourusername/email-classifier.git
cd email-classifier
pip install -r requirements.txt

# 2. 配置
cp templates/accounts.example.yaml accounts.yaml
# 编辑 accounts.yaml 添加您的凭据

# 3. 运行
python scripts/email_classifier.py --fetch --days 7 --output results.json
python scripts/frequency_analyzer.py --input results.json --output frequency_report.json
python scripts/rule_generator.py --input results.json --format gmail-labels
```

## 📚 文档

- [README.md](README.md) - 完整项目文档
- [SKILL.md](SKILL.md) - Hermes Agent skill 集成指南
- [references/](references/) - Gmail、Outlook、Lark 详细指南
- [docs/](docs/) - 架构和 API 文档

## 🏗️ 架构

```
┌─────────────────────────────────────────────────────────┐
│                   邮件分类器                              │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   获取器     │  │  分类器      │  │  分析器      │ │
│  │  (IMAP)      │  │  (规则/ML)   │  │  (频率)      │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│         │                 │                 │         │
│         └─────────────────┼─────────────────┘         │
│                           │                           │
│                  ┌────────▼────────┐                  │
│                  │   报告生成      │                  │
│                  │  (规则/导出)    │                  │
│                  └────────┬────────┘                  │
└───────────────────────────┼───────────────────────────┘
                            │
                ┌───────────┼───────────┐
                │           │           │
          ┌─────▼────┐ ┌───▼────┐ ┌───▼────┐
          │ Gmail    │ │Outlook │ │ IMAP   │
          │ 标签     │ │ 规则   │ │ 过滤器  │
          └──────────┘ └────────┘ └────────┘
```

## 📊 支持的类别

| 类别 | 描述 | 检测模式 |
|------|------|----------|
| verification_codes | OTP、密码重置 | 数字代码、安全关键词 |
| social | 社交媒体通知 | 平台特定发件人 |
| promotions | 营销邮件 | 优惠/折扣关键词 |
| work | 专业通信 | 商业域名 |
| personal | 个人通信 | 非正式模式 |
| notifications | 系统警报 | 安全/更新关键词 |
| transactions | 收据、发票 | 支付关键词 |
| forums | 社区讨论 | 论坛平台发件人 |

## 🔧 配置

### 账户设置
```yaml
accounts:
  - name: "工作"
    provider: "gmail"
    email: "work@example.com"
    imap_host: "imap.gmail.com"
    auth_type: "app_password"
    password: "your-app-password"
```

### 自定义规则
参见 [references/custom-rules-guide.md](references/custom-rules-guide.md) 获取详细的规则创建指南。

## 🧪 测试

```bash
# 运行所有测试
./scripts/run_tests.sh

# 运行覆盖率测试
python -m pytest tests/ --cov=scripts --cov-report=html

# 运行特定测试
python -m pytest tests/test_email_classifier.py -v -k verification
```

## 🔒 安全

- 所有处理都在本地进行 - 不发送数据到外部服务器
- 使用应用密码，不是普通密码
- 凭据永远不会提交到 git
- 生成的规则在应用前会经过审查

## 🤝 贡献

1. Fork 仓库
2. 创建功能分支（`git checkout -b feature/amazing-classification`）
3. 提交更改（`git commit -m '添加出色的分类功能'`）
4. 推送到分支（`git push origin feature/amazing-classification`）
5. 创建 Pull Request

## 📄 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- [Hermes Agent](https://github.com/NousResearch/hermes-agent) - Skill 框架
- 邮件提供商（Gmail、Outlook、IMAP）
- 开源分类库

## 📞 支持

- 📖 [文档](docs/)
- 💬 [讨论](https://github.com/yourusername/email-classifier/discussions)
- 🐛 [问题](https://github.com/yourusername/email-classifier/issues)

---

**注意**：此 skill 与 Hermes Agent 集成，但可独立使用。对于飞书/Lark，请使用 `lark-mail` skill。

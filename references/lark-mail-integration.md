# 飞书/Lark 邮件集成指南

**重要提示**：飞书/Lark **不支持** IMAP/SMTP 协议。请使用 `lark-mail` skill 而不是直接 IMAP 连接。

## 为什么飞书需要不同的方法

飞书/Lark 是一个专有的企业通信平台，它：
- 不暴露 IMAP/SMTP 接口
- 使用专有 API（飞书开放 API）
- 需要 OAuth 或 API 令牌认证
- 具有不同的数据结构和功能

## 推荐方法：使用 lark-mail Skill

`lark-mail` skill 提供飞书/Lark 的全面邮件功能：

### 1. 安装 lark-cli

```bash
# 遵循 lark-mail skill 设置说明
# 通常是：pip install lark-cli 或使用官方安装程序
```

### 2. 与飞书认证

```bash
# 登录飞书/Lark
lark-cli auth login --domain mail

# 这将打开浏览器进行 OAuth 授权
# 按照提示授予权限
```

### 3. 访问您的飞书邮件

```bash
# 检查认证状态
lark-cli auth status

# 查看个人资料信息
lark-cli mail user_mailboxes profile --params '{"user_mailbox_id":"me"}'
```

## 与邮件分类器的集成

虽然您不能将 IMAP 与飞书一起使用，但您可以集成分类逻辑：

### 方案一：将飞书邮件导出为 JSON

```bash
# 使用 lark-cli 获取并导出邮件
lark-cli mail +triage --folder INBOX --page-size 100 --output lark_emails.json
```

然后使用邮件分类器处理：

```bash
# 将飞书格式转换为邮件分类器格式
python scripts/converters/lark_to_classifier.py \
  --input lark_emails.json \
  --output converted_emails.json

# 运行分类
python scripts/email_classifier.py \
  --input converted_emails.json \
  --output classified_lark.json
```

### 方案二：使用飞书专用分类脚本

创建使用飞书 API 直接操作的自定义脚本：

```python
# scripts/lark_email_classifier.py
import lark_cli
from email_classifier import EmailClassifier

def classify_lark_emails():
    # 使用 lark-cli 获取邮件
    result = lark_cli.run(['mail', '+triage', '--folder', 'INBOX'])
    
    # 转换为标准格式
    emails = convert_lark_to_standard(result)
    
    # 使用现有引擎分类
    classifier = EmailClassifier()
    classifications = []
    for email in emails:
        scores = classifier.classify_email(email)
        primary_cat, confidence = classifier.get_primary_category(scores)
        classifications.append({
            'email': email,
            'category': primary_cat,
            'confidence': confidence
        })
    
    return classifications
```

## 飞书 API 速率限制

飞书 API 有限制：
- 默认速率：每分钟 50-100 次请求
- 批量操作：每次最多 50 条记录
- 建议：添加延迟和重试逻辑

## 数据格式转换

飞书邮件使用不同的数据结构。您需要：

1. 将飞书消息 ID 映射到标准字段
2. 转换发件人/收件人格式
3. 标准化日期时间
4. 提取主题和正文内容

## 安全注意事项

- ✅ 使用官方 lark-cli 工具
- ✅ 安全存储 API 令牌
- ✅ 遵守飞书 API 使用条款
- ✅ 不在代码中硬编码凭据

## 更多信息

- [飞书开放平台文档](https://open.feishu.cn/document)
- [lark-mail Skill 文档](https://github.com/yourusername/lark-mail)
- [飞书 API 速率限制](https://open.feishu.cn/document/uAjLw4CM/ukzMukzMukzM/reference/im-v1/message/list)

## 常见问题

### Q: 为什么不能用 IMAP 连接飞书？
A: 飞书是专有平台，不提供标准的 IMAP/SMTP 协议。

### Q: 我可以使用第三方 IMAP 代理吗？
A: 不建议，这违反服务条款，可能导致账户被封禁。

### Q: 如何自动化飞书邮件分类？
A: 使用 lark-cli 导出邮件，然后使用本 skill 进行分类。

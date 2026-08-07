# 故障排除指南

邮件分类器的常见问题和解决方案。

## 连接问题

### IMAP 连接失败

**错误**：`连接被拒绝`或`连接超时`

**解决方案**：
1. **检查互联网连接**：确保您有活动的互联网访问
2. **验证 IMAP 设置**：
   - Gmail：`imap.gmail.com:993`
   - Outlook：`outlook.office365.com:993`
   - iCloud：`imap.mail.me.com:993`
3. **检查防火墙**：确保端口 993 未被阻止
4. **手动测试**：
   ```bash
   openssl s_client -connect imap.gmail.com:993
   ```

### 认证失败

**错误**：`登录失败`或`凭据无效`

**解决方案**：
1. **使用应用密码**：常规密码无法与 IMAP 配合使用
   - Gmail：在 https://myaccount.google.com/apppasswords 生成应用密码
   - Outlook：使用应用密码或 OAuth
   - iCloud：使用应用专用密码
2. **检查密码格式**：应用密码通常有空格（例如，`abcd efgh ijkl mnop`）
3. **验证 2FA 已启用**：大多数提供商要求在 IMAP 访问上启用 2FA
4. **检查账户状态**：确保账户未锁定或暂停

### OAuth 问题

**错误**：`OAuth 令牌已过期`或`客户端 ID 无效`

**解决方案**：
1. **刷新令牌**：
   ```bash
   python scripts/oauth_refresh.py --refresh-token your-token
   ```
2. **重新授权**：删除缓存的令牌并重新运行 OAuth 流程
3. **检查客户端 ID**：在 OAuth 应用程序配置中验证凭据
4. **权限**：确保已授予请求的作用域

## 分类问题

### 准确性低

**问题**：邮件被分类到错误的类别

**解决方案**：
1. **审查分类规则**：查看 `references/custom-rules-guide.md`
2. **添加自定义规则**：创建特定类别的规则
3. **调整置信度阈值**：
   ```yaml
   settings:
     classification_confidence: 0.5  # 降低阈值
   ```
4. **检查模式重叠**：确保规则不冲突
5. **使用 ML 模型**：使用带标签数据的自定义分类器进行训练

### 验证码未检测到

**问题**：OTP 邮件被分类到其他类别

**解决方案**：
1. **检查模式**：确保代码模式匹配（4-8 位数字）
2. **添加发件人域名**：包含您服务的通知域名
3. **审查主题行**：检查常见模式如"您的代码是"
4. **降低 verification_codes 的阈值**：
   ```yaml
   custom_categories:
     - name: "verification_codes"
       weight: 2.0  # 提高置信度
   ```

### 误报

**问题**：常规邮件被分类为验证码

**解决方案**：
1. **添加排除模式**：
   ```yaml
   exclude_keywords:
     - "密码"
     - "重置"
     - "更新"
   ```
2. **需要多个信号**：主题、发件人和正文都必须匹配
3. **提高置信度阈值**：设置为 0.8 或更高

## 性能问题

### 处理缓慢

**问题**：分类花费太长时间

**解决方案**：
1. **减少邮件数量**：使用 `--days` 参数限制时间范围
2. **启用缓存**：在配置中设置 `cache_enabled: true`
3. **批量处理**：使用 `batch_classifier.py` 处理多个账户
4. **优化规则**：减少自定义规则数量

### 内存不足

**问题**：处理大型邮箱时内存溢出

**解决方案**：
1. **分批处理**：按时间范围处理
2. **增加内存**：
   ```bash
   python -X memlimit=1G scripts/email_classifier.py --fetch
   ```
3. **使用流式处理**：处理大文件时使用 `--stream` 选项

## 配置问题

### 配置加载失败

**错误**：`无法加载配置文件`

**解决方案**：
1. **检查 YAML 语法**：使用在线 YAML 验证器
2. **验证路径**：确保文件存在
3. **检查权限**：确保文件可读
4. **重新生成配置**：
   ```bash
   python scripts/config_generator.py --all
   ```

### 账户认证失败

**问题**：多个账户认证失败

**解决方案**：
1. **单独测试每个账户**：
   ```bash
   python scripts/email_classifier.py --test-connection --account work
   ```
2. **检查每个账户的凭据**
3. **验证每个账户的 IMAP 设置**
4. **确保每个账户的权限正确**

## 测试问题

### 测试失败

**错误**：`测试失败`

**解决方案**：
1. **检查 Python 版本**：需要 3.8 或更高版本
2. **重新安装依赖**：
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```
3. **运行特定测试**：
   ```bash
   python -m pytest tests/test_email_classifier.py -v -k verification
   ```
4. **检查测试配置**：确保 `tests/test_config.yaml` 存在

### 覆盖率低

**问题**：测试覆盖率低于 80%

**解决方案**：
1. **添加边界情况测试**
2. **测试错误处理**
3. **测试集成场景**
4. **使用覆盖率报告**：
   ```bash
   pytest tests/ --cov=scripts --cov-report=term-missing
   ```

## 常见问题

### Q: 如何重置所有配置？
A: 删除 `accounts.yaml` 和 `custom_rules.yaml`，然后重新生成：
```bash
python scripts/config_generator.py --all
```

### Q: 如何备份配置？
A: 复制配置文件到安全位置：
```bash
cp accounts.yaml accounts_backup_$(date +%Y%m%d).yaml
cp custom_rules.yaml custom_rules_backup_$(date +%Y%m%d).yaml
```

### Q: 如何处理非标准邮件服务器？
A: 在 accounts.yaml 中指定自定义 IMAP 设置：
```yaml
accounts:
  - name: "custom"
    provider: "custom"
    email: "user@example.com"
    imap_host: "mail.example.com"
    imap_port: 993
    auth_type: "app_password"
    password: "your-password"
```

### Q: 如何查看详细的调试信息？
A: 使用 `--verbose` 选项：
```bash
python scripts/email_classifier.py --fetch --verbose
```

## 获取帮助

如果以上解决方案都无法解决问题：

1. **检查现有问题**：在 GitHub Issues 中搜索
2. **创建新问题**：包含：
   - 错误消息
   - 复现步骤
   - 环境信息
   - 配置文件（脱敏后）
3. **联系维护者**：通过 GitHub Discussions

## 日志位置

调试日志默认保存在：
- Windows：`%APPDATA%\email-classifier\logs\`
- Linux/Mac：`~/.config/email-classifier/logs/`

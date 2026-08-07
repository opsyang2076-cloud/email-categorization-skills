# Gmail 设置指南 - 配置邮件分类器以使用 Gmail 账户

## 先决条件

- 启用了双因素认证的 Google 账户
- 从 Google 账户设置生成的应用密码
- 在 Gmail 设置中启用了 IMAP 访问

## 步骤 1：在 Gmail 中启用 IMAP

1. 在网页浏览器中打开 Gmail
2. 点击右上角的齿轮图标（设置）
3. 点击"查看所有设置"
4. 转到"转发和 POP/IMAP"选项卡
5. 在"IMAP 访问"下，选择"启用 IMAP"
6. 点击底部的"保存更改"

## 步骤 2：生成应用密码

**重要**：这是必需的！常规密码无法与 IMAP 配合使用。

1. 访问您的 Google 账户：https://myaccount.google.com/
2. 点击左侧边栏中的"安全"
3. 在"您登录 Google 的方式"下，点击"应用密码"
4. 如果提示，登录您的 Google 账户
5. 在"选择应用"下拉菜单中，选择"邮件"
6. 在"选择设备"下拉菜单中，选择"其他（自定义名称）"
7. 输入名称如"邮件分类器"
8. 点击"生成"
9. 复制 16 位应用密码（只显示一次！）

**注意**：安全保存此密码。您将无法再次查看它。

## 步骤 3：配置 accounts.yaml

```yaml
accounts:
  - name: "工作"
    provider: "gmail"
    email: "your.work@gmail.com"
    imap_host: "imap.gmail.com"
    imap_port: 993
    auth_type: "app_password"
    password: "abcd efgh ijkl mnop"  # 16 位应用密码，带空格
```

### Gmail IMAP 设置

| 设置 | 值 |
|------|------|
| IMAP 服务器 | `imap.gmail.com` |
| IMAP 端口 | `993` |
| SSL | 必需 |
| 认证 | 应用密码或 OAuth |

### 重要说明

- 使用应用密码（16 个字符，带空格）
- **不要**使用您的常规 Google 密码
- IMAP 主机始终是 `imap.gmail.com`
- IMAP 端口始终是 993（SSL）

## 步骤 4：测试连接

```bash
python scripts/email_classifier.py --test-connection --verbose
```

预期输出：`成功连接到 your.email@gmail.com`

## 步骤 5：运行分类

```bash
python scripts/email_classifier.py --fetch --days 7 --output gmail_results.json
```

## 故障排除

### 认证失败

**错误**：`登录失败或凭据无效`

**解决方案**：
1. 仔细检查应用密码（应该是 16 个字符，带空格）
2. 确保 Google 账户上已启用 2FA
3. 检查是否启用了"不太安全的应用访问"（不推荐，但可能需要）
4. 如果不确定，请重新生成应用密码

### IMAP 未启用

**错误**：`IMAP 访问已禁用`

**解决方案**：
1. 在 Gmail 设置中启用 IMAP（步骤 1）
2. 等待 5 分钟让更改生效
3. 如果使用工作账户，请与您的 Google Workspace 管理员联系

### 连接超时

**错误**：`连接超时`

**解决方案**：
1. 检查防火墙设置
2. 确保端口 993 未阻止
3. 尝试使用 VPN（如果需要）
4. 检查网络连接

### 权限不足

**错误**：`访问被拒绝`

**解决方案**：
1. 确保已启用 IMAP 访问
2. 检查应用密码权限
3. 对于组织账户，联系管理员

## OAuth 认证（推荐用于生产）

OAuth 比应用密码更安全。设置步骤：

1. 访问 https://console.cloud.google.com/
2. 创建新项目或选择现有项目
3. 启用 Gmail API
4. 创建 OAuth 同意屏幕
5. 创建凭据（OAuth 客户端 ID）
6. 在 accounts.yaml 中配置：

```yaml
accounts:
  - name: "gmail-oauth"
    provider: "gmail"
    email: "your.work@gmail.com"
    auth_type: "oauth"
    client_id: "your-client-id"
    client_secret: "your-client-secret"
    # OAuth 令牌将自动存储
```

## 安全建议

- ✅ 使用应用密码，不是常规密码
- ✅ 启用双因素认证
- ✅ 定期轮换应用密码
- ✅ 仅授予必要的权限
- ✅ 在本地处理数据，不发送到外部服务器

## 更多信息

- [Google 安全中心](https://security.google.com/settings/security)
- [IMAP 设置指南](https://support.google.com/mail/answer/7126229)
- [应用密码文档](https://support.google.com/accounts/answer/185833)

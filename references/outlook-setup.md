# Outlook 设置指南 - 配置邮件分类器以使用 Outlook 账户

## 先决条件

- Microsoft 365 或 Outlook.com 账户
- 应用密码或 OAuth 凭据
- IMAP 访问已启用（工作账户可能需要管理员权限）

## 步骤 1：在 Outlook 中启用 IMAP

### 对于 Outlook.com / Microsoft 365 个人版：

1. 登录 Outlook.com
2. 点击您的个人资料照片 → **查看所有 Microsoft 账户**
3. 转到**安全** → **高级安全选项**
4. 在**应用密码**下，点击**创建新的应用密码**
5. 使用生成的密码（16 个字符）

### 对于 Outlook 365（工作/学校）：

1. 联系您的 IT 管理员以启用 IMAP 访问
2. 如果没有 OAuth，请求应用密码
3. 记录您的 IMAP 服务器详情：
   - **服务器**：`outlook.office365.com`
   - **端口**：`993`
   - **SSL**：是

## 步骤 2：配置 accounts.yaml

```yaml
accounts:
  - name: "outlook-work"
    provider: "outlook"
    email: "your.name@company.com"
    imap_host: "outlook.office365.com"
    imap_port: 993
    auth_type: "app_password"
    password: "your-app-password-here"
    
  - name: "outlook-personal"
    provider: "outlook"
    email: "your.name@outlook.com"
    imap_host: "outlook.office365.com"
    imap_port: 993
    auth_type: "app_password"
    password: "your-app-password-here"
```

### Outlook IMAP 设置

| 设置 | 值 |
|------|------|
| IMAP 服务器 | `outlook.office365.com` |
| IMAP 端口 | `993` |
| SSL/TLS | 必需 |
| 认证 | OAuth2（首选）或应用密码 |

## 步骤 3：OAuth 认证（推荐用于生产）

OAuth 比应用密码更安全。以下是设置步骤：

### 3.1 创建 Azure AD 应用程序

1. 访问 [Azure 门户](https://portal.azure.com)
2. 转到**Azure Active Directory** → **应用注册**
3. 点击**新注册**
4. 输入应用程序名称（例如，"邮件分类器"）
5. 选择支持的账户类型
6. 点击**注册**

### 3.2 配置 API 权限

1. 转到**API 权限** → **添加权限**
2. 选择**Microsoft APIs** → **Office 365 Exchange Online**
3. 添加这些权限：
   - `Mail.Read`（委派）
   - `Mail.ReadWrite`（委派，可选）
4. 点击**添加权限**

### 3.3 创建客户端密钥

1. 转到**证书和密码**
2. 点击**新客户端密钥**
3. 添加描述和过期时间
4. 复制密钥值（只显示一次！）

### 3.4 为 OAuth 配置 accounts.yaml

```yaml
accounts:
  - name: "outlook-oauth"
    provider: "outlook"
    email: "your.name@company.com"
    auth_type: "oauth"
    client_id: "your-client-id"
    client_secret: "your-client-secret"
    tenant_id: "your-tenant-id"
    # OAuth 令牌将自动存储
```

## 步骤 4：测试连接

```bash
python scripts/email_classifier.py --test-connection --verbose
```

## 故障排除

### 认证失败

**错误**：`登录失败或凭据无效`

**解决方案**：
1. 检查应用密码格式
2. 确保启用了 IMAP 访问
3. 对于工作账户，联系 IT 管理员
4. 验证 OAuth 凭据

### IMAP 未启用

**错误**：`IMAP 访问已禁用`

**解决方案**：
1. 在 Outlook.com 设置中启用 IMAP
2. 对于组织账户，联系管理员
3. 等待更改生效（最多 5 分钟）

### OAuth 问题

**错误**：`OAuth 令牌已过期`或`客户端 ID 无效`

**解决方案**：
1. 刷新令牌：
   ```bash
   python scripts/oauth_refresh.py --refresh-token your-token
   ```
2. 重新授权：删除缓存的令牌并重新运行 OAuth 流程
3. 检查客户端 ID：在 OAuth 应用程序配置中验证凭据
4. 权限：确保已授予请求的作用域

## 安全建议

- ✅ 优先使用 OAuth，不是应用密码
- ✅ 定期轮换客户端密钥
- ✅ 仅请求必要的权限
- ✅ 安全存储令牌
- ✅ 在本地处理数据

## 更多信息

- [Microsoft 应用密码文档](https://support.microsoft.com/zh-cn/account-billing/在2步验证上创建应用密码-59d34e82-8a8c-4e0f-80fe-8e7c6c6c3b8f)
- [Azure AD 应用注册](https://docs.microsoft.com/zh-cn/azure/active-directory/develop/quickstart-register-app)
- [OAuth 2.0 文档](https://docs.microsoft.com/zh-cn/azure/active-directory/develop/v2-oauth2-auth-code-flow)

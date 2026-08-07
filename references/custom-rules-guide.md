# 自定义规则指南

本指南解释如何为邮件分类器创建和自定义分类规则。

## 概述

自定义规则允许您：
- 添加特定于域名的类别
- 提高您环境中的分类准确性
- 处理默认规则未涵盖的边界情况
- 按账户调整置信度阈值

## 规则结构

每个自定义规则具有如下结构：

```yaml
custom_categories:
  - name: "类别名称"
    description: "此类别代表什么"
    weight: 1.0           # 分类分数的乘数（可选）
    
    # 要匹配的关键词（不区分大小写）
    keywords:
      - "关键词1"
      - "关键词2"
    
    # 发件人域名模式（正则表达式）
    sender_domains:
      - "域名\\.com"
      - ".*@公司\\.com"
    
    # 主题行模式（正则表达式）
    subject_patterns:
      - "模式.*这里"
      - "另一个.*模式"
    
    # 正文内容模式（正则表达式）
    body_patterns:
      - "正文.*模式"
    
    # 要排除的关键词（如果存在会降低置信度）
    exclude_keywords:
      - "退订"
      - "取消订阅"
    
    # 匹配时采取的行动
    action:
      label: "自定义/类别名称"
      priority: "高"      # 高、中、低
      notify: false
      auto_archive: false
      skip_inbox: false
```

## 创建自定义类别

### 示例 1：重要客户

```yaml
custom_categories:
  - name: "重要客户"
    description: "来自 VIP 客户的邮件，需要优先关注"
    weight: 1.5  # 提高分数 50%
    
    keywords:
      - "发票"
      - "合同"
      - "法律通知"
      - "紧急"
      - "重要"
    
    sender_domains:
      - "vip-client1\\.com"
      - "enterprise-client2\\.org"
      - "partner-domain\\.net"
    
    subject_patterns:
      - "发票.*\\d{4}-\\d{2}"
      - "合同.*续订"
      - "法律.*通知"
    
    action:
      label: "重要/客户"
      priority: "高"
      notify: true
```

### 示例 2：求职申请

```yaml
custom_categories:
  - name: "求职申请"
    description: "招聘和雇佣沟通"
    weight: 1.3
    
    keywords:
      - "求职申请"
      - "候选人"
      - "面试邀请"
      - "招聘"
      - "职位"
    
    sender_domains:
      - "greenhouse.io"
      - "lever.co"
      - "workable.com"
    
    action:
      label: "求职/申请"
      priority: "中"
```

### 示例 3：家庭邮件

```yaml
custom_categories:
  - name: "家庭"
    description: "来自家人的个人邮件"
    weight: 1.2
    
    keywords:
      - "爸爸"
      - "妈妈"
      - "哥哥"
      - "姐姐"
      - "生日"
      - "婚礼"
      - "家庭聚会"
    
    sender_domains:
      - 您家人的邮箱域名
    
    action:
      label: "家庭/个人"
      priority: "高"
      notify: true
```

## 高级配置

### 置信度阈值调整

```yaml
settings:
  classification_confidence: 0.5  # 默认阈值
  verification_codes_confidence: 0.8  # 验证码需要更高置信度
```

### 排除模式

```yaml
custom_categories:
  - name: "特定类别"
    # 排除这些模式
    exclude_subjects:
      - ".* unsub.*"
      - ".* opt.out.*"
    
    exclude_senders:
      - ".*@spam\\..*"
      - ".*@massmail\\..*"
```

### 多规则优先级

当多个规则匹配时，按 `weight` 排序：
- weight > 1.0：提高优先级
- weight < 1.0：降低优先级
- 默认 weight = 1.0

## 规则测试

测试您的自定义规则：

```bash
# 使用示例邮件测试
echo '{
  "subject": "您的测试邮件主题",
  "from": "test@example.com",
  "body": "测试邮件正文内容"
}' | python scripts/email_classifier.py --test

# 查看所有匹配的类别
python scripts/email_classifier.py --test --verbose
```

## 故障排除

### 规则不匹配

**问题**：邮件未分类到预期类别

**解决方案**：
1. 检查关键词拼写
2. 验证正则表达式语法
3. 确保发件人域名正确
4. 增加 weight 值

### 误报

**问题**：常规邮件被错误分类

**解决方案**：
1. 添加 `exclude_keywords`
2. 使用更具体的模式
3. 降低 weight 值
4. 添加排除条件

### 性能问题

**问题**：规则匹配太慢

**解决方案**：
1. 减少规则数量
2. 简化正则表达式
3. 优先检查常见模式
4. 使用缓存

## 最佳实践

1. **从简单开始**：先添加几个规则，然后逐步增加
2. **测试规则**：使用示例邮件测试每个规则
3. **记录变更**：在注释中记录为什么添加规则
4. **定期审查**：检查规则是否仍然相关
5. **备份配置**：定期备份 custom_rules.yaml

## 配置位置

将自定义规则文件保存在：
- 项目根目录：`custom_rules.yaml`
- 配置目录：`.config/email-classifier/rules.yaml`

## 更多信息

- [规则生成器文档](../scripts/rule_generator.py)
- [分类器文档](../scripts/email_classifier.py)
- [示例规则](custom_rules.example.yaml)

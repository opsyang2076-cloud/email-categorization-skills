#!/usr/bin/env python3
"""
邮件分类器 - 主分类引擎
根据内容、发件人和模式自动将邮件分类到各个类别。
"""

import imaplib
import email as email_module
import re
import json
import yaml
import os
import sys
import argparse
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from typing import Dict, List, Tuple, Optional
import logging

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EmailClassifier:
    """主邮件分类引擎。"""
    
    # 预定义类别及其匹配模式
    CATEGORIES = {
        "verification_codes": {
            "keywords": [
                "verification", "code", "otp", "password reset", "login code",
                "2fa", "two-factor", "auth code", "security code", "confirmation code",
                "verify your", "your code is", "reset your password", "login attempt"
            ],
            "sender_patterns": [
                r".*@noreply\..*",
                r".*@no-reply\..*",
                r".*@alerts\..*",
                r".*@security\..*",
                r".*@notifications\.*"
            ],
            "subject_patterns": [
                r"verification code",
                r"your code is",
                r"password reset",
                r"login code",
                r"two-factor authentication",
                r"confirm your email"
            ],
            "body_patterns": [
                r"\b\d{4,8}\b",  # 4-8 位数字代码
                r"enter this code",
                r"your verification code is"
            ],
            "priority": 1
        },
        "social": {
            "keywords": [
                "followed you", "mentioned you", "liked your", "commented on",
                "new follower", "friend request", "connect", "linkedin",
                "twitter", "facebook", "instagram", "social"
            ],
            "sender_patterns": [
                r".*@linkedin\.com",
                r".*@twitter\.com",
                r".*@facebook\.com",
                r".*@instagram\.com",
                r".*@pinterest\.com"
            ],
            "subject_patterns": [
                r"new follower",
                r"you have a new",
                r"someone mentioned",
                r"invitation to connect"
            ],
            "priority": 2
        },
        "promotions": {
            "keywords": [
                "special offer", "discount", "sale", "deal", "coupon",
                "limited time", "subscribe", "newsletter", "weekly digest",
                "monthly update", "promotional", "marketing"
            ],
            "sender_patterns": [
                r".*@newsletter\..*",
                r".*@promo\..*",
                r".*@deals\..*",
                r".*@sales\..*"
            ],
            "subject_patterns": [
                r"special offer",
                r"don't miss",
                r"exclusive deal",
                r"subscribe to receive"
            ],
            "priority": 3
        },
        "work": {
            "keywords": [
                "project", "meeting", "deadline", "report", "invoice",
                "contract", "proposal", "quarterly", "annual", "review",
                "presentation", "agenda", "minutes"
            ],
            "sender_patterns": [
                r".*@company\.com",
                r".*@work\.com",
                r".*@business\.com"
            ],
            "subject_patterns": [
                r"meeting",
                r"project update",
                r"deadline",
                r"report due"
            ],
            "priority": 4
        },
        "personal": {
            "keywords": [
                "family", "friend", "birthday", "wedding", "party",
                "hello", "hi", "hey", "how are you", "catch up"
            ],
            "subject_patterns": [
                r"birthday",
                r"wedding invitation",
                r"let's catch up"
            ],
            "priority": 5
        },
        "notifications": {
            "keywords": [
                "alert", "warning", "update available", "security",
                "suspicious", "login from", "new device", "password changed"
            ],
            "sender_patterns": [
                r".*@apple\.com",
                r".*@google\.com",
                r".*@microsoft\.com"
            ],
            "subject_patterns": [
                r"security alert",
                r"new login",
                r"password changed",
                r"update available"
            ],
            "priority": 6
        },
        "transactions": {
            "keywords": [
                "receipt", "invoice", "order confirmation", "payment",
                "purchase", "transaction", "billing", "subscription",
                "order #", "order number"
            ],
            "sender_patterns": [
                r".*@amazon\.com",
                r".*@stripe\.com",
                r".*@paypal\.com",
                r".*@shopify\.com"
            ],
            "subject_patterns": [
                r"order confirmation",
                r"receipt",
                r"your invoice",
                r"payment received"
            ],
            "priority": 7
        },
        "forums": {
            "keywords": [
                "reply", "topic", "thread", "discussion", "upvoted",
                "awarded", "badge", "stackoverflow", "reddit"
            ],
            "sender_patterns": [
                r".*@reddit\.com",
                r".*@stackoverflow\.com",
                r".*@discourse\..*"
            ],
            "subject_patterns": [
                r"new reply",
                r"someone replied",
                r"your question"
            ],
            "priority": 8
        }
    }
    
    # 频率阈值定义
    FREQUENCY_LEVELS = {
        "daily_high": {"min": 10, "max": float('inf')},
        "daily_medium": {"min": 1, "max": 9},
        "daily_low": {"min": 0.1, "max": 0.9},
        "weekly_sporadic": {"min": 0, "max": 0.09}
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """使用可选的配置文件初始化分类器。"""
        self.config = self._load_config(config_path)
        self.classification_results = {}
        self.frequency_data = defaultdict(list)
        
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """从 YAML 文件加载配置。"""
        default_config = {
            "confidence_threshold": 0.7,
            "analysis_days": 30,
            "low_frequency_threshold": 1,
            "enable_ml": False,
            "batch_size": 100,
            "cache_enabled": True,
            "cache_dir": os.path.expanduser("~/.email_classifier_cache")
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    custom_config = yaml.safe_load(f)
                    default_config.update(custom_config)
                logger.info(f"已从 {config_path} 加载配置")
            except Exception as e:
                logger.warning(f"加载配置失败: {e}，使用默认配置")
        
        return default_config
    
    def connect_to_imap(self, account: Dict) -> imaplib.IMAP4_SSL:
        """建立到电子邮件账户的 IMAP 连接。"""
        try:
            logger.info(f"正在连接到 {account['email']}...")
            
            if account.get('provider') == 'lark':
                logger.warning("飞书/Lark 使用 lark-cli，不使用 IMAP。请使用 lark-mail skill。")
                return None
            
            conn = imaplib.IMAP4_SSL(
                account['imap_host'],
                account.get('imap_port', 993)
            )
            
            # 认证
            if account.get('auth_type') == 'oauth':
                # OAuth 处理（特定于提供商）
                logger.warning("此提供商的 OAuth 认证尚未实现")
                return None
            else:
                conn.login(account['email'], account['password'])
            
            logger.info(f"成功连接到 {account['email']}")
            return conn
            
        except Exception as e:
            logger.error(f"{account['email']} 连接失败: {e}")
            raise
    
    def fetch_emails(self, conn: imaplib.IMAP4_SSL, days: int = 7, batch_size: int = 100) -> List[Dict]:
        """从收件箱获取最近的邮件。"""
        emails = []
        
        try:
            conn.select('INBOX')
            
            # 计算日期范围
            since_date = (datetime.now() - timedelta(days=days)).strftime('%d-%b-%Y')
            logger.info(f"正在获取 {since_date} 以来的邮件")
            
            # 搜索最近的邮件
            status, messages = conn.search(None, f'SINCE {since_date}')
            
            if status != 'OK':
                logger.error("邮件搜索失败")
                return emails
            
            email_ids = messages[0].split()
            total = len(email_ids)
            logger.info(f"找到 {total} 封邮件待处理")
            
            # 分批处理
            for i in range(0, min(total, days * 50), batch_size):  # 假设每天最多 50 封邮件
                batch = email_ids[i:i+batch_size]
                logger.info(f"正在处理批次 {i//batch_size + 1}")
                
                for email_id in batch:
                    try:
                        status, msg_data = conn.fetch(email_id, '(RFC822)')
                        if status == 'OK':
                            raw_email = msg_data[0][1]
                            email_obj = email.message_from_bytes(raw_email)
                            
                            email_info = self._parse_email(email_obj, email_id.decode())
                            if email_info:
                                emails.append(email_info)
                                
                    except Exception as e:
                        logger.warning(f"获取邮件 {email_id} 失败: {e}")
                        continue
                
                if len(emails) >= days * 50:  # 安全限制
                    break
                    
        except Exception as e:
            logger.error(f"获取邮件时出错: {e}")
        finally:
            try:
                conn.logout()
            except:
                pass
        
        return emails
    
    def _parse_email(self, msg: email_module.message.Message, email_id: str) -> Optional[Dict]:
        """从电子邮件消息中提取相关字段。"""
        try:
            subject = self._decode_header(msg.get('Subject', ''))
            from_addr = self._decode_header(msg.get('From', ''))
            to_addr = self._decode_header(msg.get('To', ''))
            date_str = msg.get('Date', '')
            body = self._extract_body(msg)
            
            # 解析日期
            try:
                date = email.utils.parsedate_to_datetime(date_str)
            except:
                date = datetime.now()
            
            return {
                'id': email_id,
                'subject': subject,
                'from': from_addr,
                'to': to_addr,
                'date': date.isoformat(),
                'body_preview': body[:500] if body else '',
                'has_attachments': len(msg.get_all('attachment')) > 0 if msg.get_all('attachment') else False
            }
            
        except Exception as e:
            logger.warning(f"解析邮件 {email_id} 失败: {e}")
            return None
    
    def _decode_header(self, header: str) -> str:
        """解码 MIME 编码的头部。"""
        if not header:
            return ''
        
        decoded = email.header.decode_header(header)
        result = []
        
        for part, charset in decoded:
            if isinstance(part, bytes):
                charset = charset or 'utf-8'
                try:
                    result.append(part.decode(charset))
                except:
                    result.append(part.decode('utf-8', errors='replace'))
            else:
                result.append(part)
        
        return ''.join(result)
    
    def _extract_body(self, msg: email_module.message.Message) -> str:
        """从电子邮件中提取纯文本正文。"""
        body = ''
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    try:
                        charset = part.get_content_charset() or 'utf-8'
                        body = part.get_payload(decode=True).decode(charset)
                        break
                    except:
                        continue
        else:
            try:
                charset = msg.get_content_charset() or 'utf-8'
                body = msg.get_payload(decode=True).decode(charset)
            except:
                body = ''
        
        return body
    
    def classify_email(self, email_data: Dict) -> Dict[str, float]:
        """将单封邮件分类到各个类别。"""
        scores = {}
        
        subject = email_data.get('subject', '').lower()
        from_addr = email_data.get('from', '').lower()
        body = email_data.get('body_preview', '').lower()
        combined_text = f"{subject} {from_addr} {body}"
        
        for category, rules in self.CATEGORIES.items():
            score = 0.0
            max_score = 0.0
            
            # 检查关键词
            for keyword in rules.get('keywords', []):
                max_score += 1
                if keyword.lower() in combined_text:
                    score += 1
            
            # 检查发件人模式
            for pattern in rules.get('sender_patterns', []):
                max_score += 1
                if re.search(pattern, from_addr, re.IGNORECASE):
                    score += 1
            
            # 检查主题模式
            for pattern in rules.get('subject_patterns', []):
                max_score += 1
                if re.search(pattern, subject, re.IGNORECASE):
                    score += 1
            
            # 检查正文模式
            for pattern in rules.get('body_patterns', []):
                max_score += 1
                if re.search(pattern, body, re.IGNORECASE):
                    score += 1
            
            # 应用优先级权重
            priority = rules.get('priority', 5)
            if max_score > 0:
                final_score = (score / max_score) * (11 - priority) / 10
            else:
                final_score = 0.0
            
            scores[category] = final_score
        
        # 验证码特殊处理
        scores['verification_codes'] = self._calculate_verification_score(email_data, combined_text)
        
        return scores
    
    def _calculate_verification_score(self, email_data: Dict, text: str) -> float:
        """计算验证码的特定得分。"""
        score = 0.0
        
        # 检查主题或正文中的数字代码
        code_patterns = [
            r'\b\d{4,8}\b',  # 4-8 位数字代码
            r'your code is\s*\d+',
            r'code:\s*\d+',
            r'otp:\s*\d+'
        ]
        
        for pattern in code_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                score += 0.5
        
        # 检查主题关键词
        subject_keywords = ['verification', 'code', 'otp', 'password reset', 'login']
        for keyword in subject_keywords:
            if keyword in email_data.get('subject', '').lower():
                score += 0.3
        
        # 检查发件人模式
        sender = email_data.get('from', '').lower()
        if any(x in sender for x in ['noreply', 'no-reply', 'alerts', 'security', 'notifications']):
            score += 0.2
        
        return min(score, 1.0)
    
    def get_primary_category(self, scores: Dict[str, float], threshold: float = 0.3) -> Tuple[str, float]:
        """获取置信度最高的主要类别。"""
        if not scores:
            return ('uncategorized', 0.0)
        
        # 找到得分最高的类别
        best_category = 'uncategorized'
        best_score = 0.0
        
        for category, score in scores.items():
            if score > best_score and score >= threshold:
                best_category = category
                best_score = score
        
        return best_category, best_score
    
    def analyze_frequency(self, emails: List[Dict], account_name: str) -> Dict:
        """分析账户的邮件频率。"""
        if not emails:
            return {
                'account': account_name,
                'total_emails': 0,
                'daily_average': 0,
                'frequency_level': 'no_data',
                'recommendation': '无邮件可分析'
            }
        
        # 解析日期并按天统计
        date_counts = Counter()
        for email in emails:
            try:
                date = datetime.fromisoformat(email['date'])
                date_counts[date.strftime('%Y-%m-%d')] += 1
            except:
                continue
        
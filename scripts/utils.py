"""
工具函数 - 邮件分类器的辅助功能
提供配置加载、数据转换、格式化等通用功能。
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml

logger = logging.getLogger(__name__)


def load_config(config_path: str) -> Dict:
    """从 YAML 文件加载配置。
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        配置字典
    """
    if not os.path.exists(config_path):
        logger.warning(f"配置文件不存在: {config_path}")
        return {}
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def save_config(config: Dict, config_path: str):
    """保存配置到 YAML 文件。
    
    Args:
        config: 配置字典
        config_path: 输出文件路径
    """
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    logger.info(f"配置已保存到 {config_path}")


def convert_lark_to_standard(lark_data: Dict) -> Dict:
    """将飞书/Lark 邮件格式转换为标准格式。
    
    Args:
        lark_data: 飞书邮件数据
        
    Returns:
        标准格式的邮件数据
    """
    standard_emails = []
    
    for msg in lark_data.get('messages', []):
        standard_email = {
            'id': msg.get('message_id', ''),
            'subject': msg.get('subject', '无主题'),
            'from': msg.get('sender', {}).get('email', ''),
            'to': ', '.join([r.get('email', '') for r in msg.get('receivers', [])]),
            'date': msg.get('created_time', ''),
            'body_preview': msg.get('body', '')[:500],
            'has_attachments': len(msg.get('attachments', [])) > 0
        }
        standard_emails.append(standard_email)
    
    return {'emails': standard_emails}


def convert_outlook_to_standard(outlook_data: Dict) -> Dict:
    """将 Outlook 邮件格式转换为标准格式。
    
    Args:
        outlook_data: Outlook 邮件数据
        
    Returns:
        标准格式的邮件数据
    """
    standard_emails = []
    
    for msg in outlook_data.get('items', []):
        standard_email = {
            'id': msg.get('id', ''),
            'subject': msg.get('subject', '无主题'),
            'from': msg.get('from', {}).get('emailAddress', ''),
            'to': ', '.join([r.get('emailAddress', '') for r in msg.get('toRecipients', [])]),
            'date': msg.get('receivedDateTime', ''),
            'body_preview': msg.get('body', {}).get('content', '')[:500],
            'has_attachments': len(msg.get('attachments', [])) > 0
        }
        standard_emails.append(standard_email)
    
    return {'emails': standard_emails}


def format_email_date(date_str: str) -> str:
    """格式化电子邮件日期为 ISO 格式。
    
    Args:
        date_str: 原始日期字符串
        
    Returns:
        ISO 格式的日期字符串
    """
    if not date_str:
        return datetime.now().isoformat()
    
    # 尝试多种日期格式
    formats = [
        '%a, %d %b %Y %H:%M:%S %z',
        '%d %b %Y %H:%M:%S %z',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%d'
    ]
    
    for fmt in formats:
        try:
            date_obj = datetime.strptime(date_str, fmt)
            return date_obj.isoformat()
        except ValueError:
            continue
    
    # 如果所有格式都失败，返回原始值
    return date_str


def sanitize_filename(filename: str) -> str:
    """清理文件名，移除不安全字符。
    
    Args:
        filename: 原始文件名
        
    Returns:
        清理后的文件名
    """
    # 移除或替换不安全字符
    unsafe_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    
    # 限制长度
    if len(filename) > 100:
        filename = filename[:100]
    
    return filename


def generate_timestamp() -> str:
    """生成当前时间戳。
    
    Returns:
        ISO 格式的时间戳
    """
    return datetime.now().isoformat()


def truncate_string(text: str, max_length: int = 500) -> str:
    """截断字符串到指定长度。
    
    Args:
        text: 原始文本
        max_length: 最大长度
        
    Returns:
        截断后的文本
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + '...'


def merge_configs(base_config: Dict, override_config: Dict) -> Dict:
    """合并两个配置字典，override_config 优先。
    
    Args:
        base_config: 基础配置
        override_config: 覆盖配置
        
    Returns:
        合并后的配置
    """
    merged = base_config.copy()
    merged.update(override_config)
    return merged


def calculate_statistics(values: List[float]) -> Dict:
    """计算统计数据。
    
    Args:
        values: 数值列表
        
    Returns:
        统计结果字典
    """
    if not values:
        return {
            'count': 0,
            'sum': 0,
            'mean': 0,
            'min': 0,
            'max': 0
        }
    
    return {
        'count': len(values),
        'sum': sum(values),
        'mean': sum(values) / len(values),
        'min': min(values),
        'max': max(values)
    }


def validate_email(email: str) -> bool:
    """验证电子邮件地址格式。
    
    Args:
        email: 电子邮件地址
        
    Returns:
        是否有效
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

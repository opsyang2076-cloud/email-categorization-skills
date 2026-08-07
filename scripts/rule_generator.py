#!/usr/bin/env python3
"""
规则生成器 - 为邮件客户端生成分类规则
支持 Gmail 标签、IMAP 规则和自定义格式。
"""

import json
import yaml
import argparse
import logging
from datetime import datetime
from collections import Counter, defaultdict
from typing import Dict, List, Optional
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RuleGenerator:
    """为不同客户端生成电子邮件分类规则。"""
    
    def __init__(self):
        self.supported_formats = ['gmail-labels', 'imap-rules', 'outlook-rules', 'yaml', 'csv']
        
    def generate_rules(self, classification_data: Dict, output_format: str = 'yaml') -> Dict:
        """基于分类数据生成规则。"""
        if output_format not in self.supported_formats:
            raise ValueError(f"不支持的格式: {output_format}。使用以下之一: {self.supported_formats}")
        
        generators = {
            'yaml': self._generate_yaml_rules,
            'gmail-labels': self._generate_gmail_rules,
            'imap-rules': self._generate_imap_rules,
            'outlook-rules': self._generate_outlook_rules,
            'csv': self._generate_csv_rules
        }
        
        return generators[output_format](classification_data)
    
    def _generate_yaml_rules(self, data: Dict) -> Dict:
        """生成 YAML 格式的规则。"""
        rules = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'format': 'yaml',
                'source': 'email-classifier'
            },
            'rules': []
        }
        
        # 提取分类模式
        if 'results' in data:
            for account_name, account_data in data['results'].items():
                classifications = account_data.get('classifications', [])
                
                # 按主要类别分组
                category_rules = {}
                for classification in classifications:
                    primary_cat = classification.get('primary_category', '未分类')
                    email = classification.get('email', {})
                    
                    if primary_cat not in category_rules:
                        category_rules[primary_cat] = {
                            'patterns': set(),
                            'senders': set(),
                            'subjects': set(),
                            'count': 0
                        }
                    
                    category_rules[primary_cat]['count'] += 1
                    
                    # 提取模式
                    subject = email.get('subject', '')
                    sender = email.get('from', '')
                    
                    if subject:
                        category_rules[primary_cat]['subjects'].add(subject[:50])
                    if sender:
                        category_rules[primary_cat]['senders'].add(sender)
                
                # 转换为规则
                for category, info in category_rules.items():
                    if info['count'] >= 3:  # 只为有足够的类别创建规则
                        rules['rules'].append({
                            'name': f"{account_name}_{category}",
                            'category': category,
                            'conditions': {
                                'subject_contains': list(info['subjects'])[:10],
                                'sender_matches': list(info['senders'])[:10]
                            },
                            'action': f'label_as_{category}',
                            'confidence': '高' if info['count'] > 10 else '中'
                        })
        
        return rules
    
    def _generate_gmail_rules(self, data: Dict) -> Dict:
        """生成 Gmail 过滤器规则。"""
        filters = []
        
        if 'results' not in data:
            return {'format': 'gmail-filters', 'filters': filters}
        
        # 跨所有账户收集类别模式
        category_patterns = defaultdict(lambda: {'senders': set(), 'subjects': set()})
        
        for account_name, account_data in data['results'].items():
            classifications = account_data.get('classifications', [])
            
            for classification in classifications:
                primary_cat = classification.get('primary_category', '未分类')
                email = classification.get('email', {})
                
                subject = email.get('subject', '')
                sender = email.get('from', '')
                
                if subject:
                    category_patterns[primary_cat]['subjects'].add(subject.lower())
                if sender:
                    category_patterns[primary_cat]['senders'].add(sender.lower())
        
        # 为每个类别创建过滤器
        for category, patterns in category_patterns.items():
            if category == '未分类':
                continue
            
            filter_conditions = {}
            
            # 添加发件人条件
            senders = list(patterns['senders'])[:5]
            if senders:
                filter_conditions['has_words'] = ' '.join(senders)
            
            # 添加主题条件
            subjects = list(patterns['subjects'])[:5]
            if subjects:
                filter_conditions['subject_contains'] = subjects
            
            if filter_conditions:
                filters.append({
                    'create_filter': True,
                    'criteria': filter_conditions,
                    'actions': {
                        'apply_label': f'分类/{category.replace("_", " ").title()}',
                        'skip_inbox': category in ['promotions', 'forums'],
                        'mark_as_read': category in ['promotions', 'social']
                    }
                })
        
        return {
            'format': 'gmail-filters',
            'generated_at': datetime.now().isoformat(),
            'filters': filters,
            'import_instructions': '转到 Gmail 设置 > 过滤器和已屏蔽的地址 > 创建新过滤器'
        }
    
    def _generate_imap_rules(self, data: Dict) -> Dict:
        """生成 IMAP 服务器端规则。"""
        rules = []
        
        if 'results' not in data:
            return {'format': 'imap-rules', 'rules': rules}
        
        # 收集模式
        category_data = defaultdict(lambda: {'senders': set(), 'subjects': set()})
        
        for account_name, account_data in data['results'].items():
            classifications = account_data.get('classifications', [])
            
            for classification in classifications:
                primary_cat = classification.get('primary_category', '未分类')
                email = classification.get('email', {})
                
                subject = email.get('subject', '')
                sender = email.get('from', '')
                
                if subject:
                    category_data[primary_cat]['subjects'].add(subject)
                if sender:
                    category_data[primary_cat]['senders'].add(sender)
        
        # 生成 IMAP 规则
        for category, patterns in category_data.items():
            if category == '未分类':
                continue
            
            conditions = []
            
            # 发件人条件
            for sender in list(patterns['senders'])[:3]:
                conditions.append(f'FROM "{sender}"')
            
            # 主题条件
            for subject in list(patterns['subjects'])[:3]:
                conditions.append(f'SUBJECT "{subject[:30]}"')
            
            if conditions:
                rules.append({
                    'name': f"classify_{category}",
                    'enabled': True,
                    'priority': 10,
                    'conditions': ' AND '.join(conditions[:5]),
                    'actions': [
                        f'ADD_FLAG \\{category}',
                        f'MOVE_TO "{category.title()}"'
                    ]
                })
        
        return {
            'format': 'imap-rules',
            'generated_at': datetime.now().isoformat(),
            'rules': rules,
            'notes': '通过您的邮件客户端或 IMAP 服务器配置应用这些规则'
        }
    
    def _generate_outlook_rules(self, data: Dict) -> Dict:
        """生成 Outlook VBA/规则格式。"""
        rules = []
        
        if 'results' not in data:
            return {'format': 'outlook-rules', 'rules': rules}
        
        category_data = defaultdict(lambda: {'senders': set(), 'subjects': set()})
        
        for account_name, account_data in data['results'].items():
            classifications = account_data.get('classifications', [])
            
            for classification in classifications:
                primary_cat = classification.get('primary_category', '未分类')
                email = classification.get('email', {})
                
                subject = email.get('subject', '')
                sender = email.get('from', '')
                
                if subject:
                    category_data[primary_cat]['subjects'].add(subject)
                if sender:
                    category_data[primary_cat]['senders'].add(sender)
        
        for category, patterns in category_data.items():
            if category == '未分类':
                continue
            
            conditions = []
            for sender in list(patterns['senders'])[:3]:
                conditions.append(f'from "{sender}"')
            for subject in list(patterns['subjects'])[:3]:
                conditions.append(f'subject contains "{subject[:30]}"')
            
            rules.append({
                'name': f"分类为 {category.title()}",
                'enabled': True,
                'conditions': ' AND '.join(conditions[:3]),
                'actions': [
                    f'Move to folder: {category.title()}',
                    f'Apply category: {category.title()}'
                ]
            })
        
        return {
            'format': 'outlook-rules',
            'generated_at': datetime.now().isoformat(),
            'rules': rules,
            'vba_code': self._generate_outlook_vba(rules),
            'notes': '通过 Outlook 规则向导导入或运行 VBA 宏'
        }
    
    def _generate_outlook_vba(self, rules: List[Dict]) -> str:
        """为 Outlook 规则生成 VBA 代码。"""
        vba_lines = [
            "Sub 应用邮件分类()",
            "    Dim olApp As Outlook.Application",
            "    Dim ns As Outlook.NameSpace",
            "    Dim inbox As Outlook.Folder",
            "    Dim mail As Outlook.MailItem",
            "    Dim rule As Outlook.Rule",
            "",
            "    Set olApp = Outlook.Application",
            "    Set ns = olApp.GetNamespace(\"MAPI\")",
            "    Set inbox = ns.GetDefaultFolder(olFolderInbox)",
            "",
            "    For Each mail In inbox.Items",
            "        If TypeName(mail) = \"MailItem\" Then",
            "            ' 基于规则应用分类",
            "            ' （简化 - 需要完整的规则匹配逻辑）",
            "        End If",
            "    Next mail",
            "",
            "    Set mail = Nothing",
            "    Set inbox = Nothing",
            "    Set ns = Nothing",
            "    Set olApp = Nothing",
            "End Sub"
        ]
        
        return '\n'.join(vba_lines)
    
    def _generate_csv_rules(self, data: Dict) -> Dict:
        """生成用于电子表格导入的 CSV 格式规则。"""
        rows = [['规则名称', '类别', '条件类型', '条件值', '操作', '优先级']]
        
        if 'results' not in data:
            return {'format': 'csv', 'rows': rows}
        
        row_num = 1
        for account_name, account_data in data['results'].items():
            classifications = account_data.get('classifications', [])
            
            # 按类别分组
            category_senders = defaultdict(set)
            category_subjects = defaultdict(set)
            
            for classification in classifications:
                primary_cat = classification.get('primary_category', '未分类')
                email = classification.get('email', {})
                
                sender = email.get('from', '')
                subject = email.get('subject', '')
                
                if sender:
                    category_senders[primary_cat].add(sender)
                if subject:
                    category_subjects[primary_cat].add(subject)
            
            for category in category_senders.keys():
                if category == '未分类':
                    continue
                
                # 添加基于发件人的规则
                for sender in list(category_senders[category])[:3]:
                    rows.append([
                        f"规则_{row_num}",
                        category,
                        '发件人',
                        sender,
                        f'标记为 {category}',
                        '中'
                    ])
                    row_num += 1
                
                # 添加基于主题的规则
                for subject in list(category_subjects[category])[:3]:
                    rows.append([
                        f"规则_{row_num}",
                        category,
                        '主题包含',
                        subject[:50],
                        f'标记为 {category}',
                        '低'
                    ])
                    row_num += 1
        
        return {
            'format': 'csv',
            'generated_at': datetime.now().isoformat(),
            'rows': rows,
            'notes': '导入到 Gmail 过滤器或邮件客户端规则系统'
        }


def main():
    parser = argparse.ArgumentParser(
        description='生成电子邮件分类规则',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 生成 YAML 规则
  python rule_generator.py --input classified_emails.json --format yaml --output rules.yaml
  
  # 生成 Gmail 标签
  python rule_generator.py --input classified_emails.json --format gmail-labels --output gmail_rules.json
  
  # 生成 IMAP 规则
  python rule_generator.py --input classified_emails.json --format imap-rules --output imap_rules.json
        """
    )
    
    parser.add_argument('--input', '-i', required=True, help='输入分类 JSON 文件')
    parser.add_argument('--format', '-f', default='yaml', 
                       choices=['yaml', 'gmail-labels', 'imap-rules', 'outlook-rules', 'csv'],
                       help='输出格式（默认：yaml）')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # 加载分类数据
        with open(args.input, 'r', encoding='utf-8') as f:
            classification_data = json.load(f)
        
        # 生成规则
        generator = RuleGenerator()
        rules = generator.generate_rules(classification_data, args.format)
        
        # 保存输出
        output_path = args.output or f"classification_rules_{args.format}.{['yaml', 'json', 'csv'][['yaml', 'gmail-labels', 'imap-rules', 'outlook-rules', 'csv'].index(args.format)]}"
        
        if args.format == 'yaml':
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(rules, f, default_flow_style=False, allow_unicode=True)
        else:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(rules, f, indent=2, ensure_ascii=False)
        
        logger.info(f"规则已生成并保存到 {output_path}")
        
        # 打印摘要
        print("\n" + "="*60)
        print("规则生成摘要")
        print("="*60)
        print(f"格式: {args.format}")
        print(f"输出: {output_path}")
        
        if args.format in ['yaml', 'gmail-labels', 'imap-rules', 'outlook-rules']:
            rule_count = len(rules.get('rules', [])) if 'rules' in rules else len(rules.get('filters', []))
            print(f"生成的规则数: {rule_count}")
        elif args.format == 'csv':
            print(f"生成的 CSV 行数: {len(rules.get('rows', [])) - 1}")  # 排除表头
        
        if 'notes' in rules:
            print(f"\n说明: {rules['notes']}")
        
        print("="*60)
        
    except FileNotFoundError:
        logger.error(f"未找到输入文件: {args.input}")
        sys.exit(1)
    except json.JSONDecodeError:
        logger.error(f"输入文件中的 JSON 无效: {args.input}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"错误: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

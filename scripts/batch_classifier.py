#!/usr/bin/env python3
"""
批量邮件分类器 - 以批量模式处理多个账户
编排跨多个电子邮件账户的获取、分类和分析。
"""

import yaml
import json
import argparse
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional
from email_classifier import EmailClassifier
from frequency_analyzer import FrequencyAnalyzer
from rule_generator import RuleGenerator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BatchClassifier:
    """批量处理多个电子邮件账户。"""
    
    def __init__(self, config_path: str):
        """使用配置文件初始化。"""
        self.config = self._load_config(config_path)
        self.classifier = EmailClassifier()
        self.frequency_analyzer = FrequencyAnalyzer(
            low_threshold=self.config.get('low_frequency_threshold', 1.0)
        )
        self.rule_generator = RuleGenerator()
        
    def _load_config(self, config_path: str) -> Dict:
        """加载批量处理配置。"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def process_all_accounts(self, days: int = 7, batch_size: int = 100) -> Dict:
        """处理所有配置的账户。"""
        accounts = self.config.get('accounts', [])
        results = {
            'metadata': {
                'started_at': datetime.now().isoformat(),
                'total_accounts': len(accounts),
                'config_file': self.config.get('file_path', '未知')
            },
            'accounts': {},
            'errors': []
        }
        
        logger.info(f"开始为 {len(accounts)} 个账户进行批量处理")
        
        for account in accounts:
            account_name = account.get('name', account.get('email', '未知'))
            logger.info(f"正在处理账户: {account_name}")
            
            try:
                account_result = self._process_single_account(account, days, batch_size)
                results['accounts'][account_name] = account_result
                
            except Exception as e:
                logger.error(f"处理账户 {account_name} 失败: {e}")
                results['errors'].append({
                    'account': account_name,
                    'error': str(e)
                })
        
        results['metadata']['completed_at'] = datetime.now().isoformat()
        results['metadata']['successful_accounts'] = len(results['accounts'])
        results['metadata']['failed_accounts'] = len(results['errors'])
        
        return results
    
    def _process_single_account(self, account: Dict, days: int, batch_size: int) -> Dict:
        """处理单个电子邮件账户。"""
        account_name = account.get('name', account.get('email', '未知'))
        
        # 连接并获取
        conn = self.classifier.connect_to_imap(account)
        if not conn:
            raise Exception(f"无法连接到 {account_name}")
        
        # 获取邮件
        emails = self.classifier.fetch_emails(conn, days=days, batch_size=batch_size)
        logger.info(f"从 {account_name} 获取了 {len(emails)} 封邮件")
        
        # 分类邮件
        classifications = []
        for email_data in emails:
            scores = self.classifier.classify_email(email_data)
            primary_cat, confidence = self.classifier.get_primary_category(scores)
            classifications.append({
                'email': email_data,
                'scores': scores,
                'primary_category': primary_cat,
                'confidence': confidence
            })
        
        return {
            'email_address': account.get('email', ''),
            'emails': emails,
            'classifications': classifications,
            'fetch_stats': {
                'total_fetched': len(emails),
                'days_analyzed': days,
                'classification_rate': len(classifications) / max(len(emails), 1)
            }
        }
    
    def generate_comprehensive_report(self, batch_results: Dict) -> Dict:
        """从批量结果生成综合报告。"""
        # 准备频率分析器的数据
        classification_data = {
            'metadata': batch_results['metadata'],
            'results': batch_results['accounts']
        }
        
        # 分析频率
        frequency_analysis = self.frequency_analyzer.analyze_all_accounts(classification_data)
        
        # 生成规则
        yaml_rules = self.rule_generator.generate_rules(classification_data, 'yaml')
        gmail_rules = self.rule_generator.generate_rules(classification_data, 'gmail-labels')
        
        # 编译最终报告
        report = {
            'generated_at': datetime.now().isoformat(),
            'batch_summary': {
                'total_accounts': len(batch_results['accounts']),
                'successful': batch_results['metadata']['successful_accounts'],
                'failed': batch_results['metadata']['failed_accounts'],
                'total_emails_processed': sum(
                    len(acc.get('emails', []))
                    for acc in batch_results['accounts'].values()
                )
            },
            'classification_summary': frequency_analysis,
            'rules': {
                'yaml': yaml_rules,
                'gmail_labels': gmail_rules
            },
            'errors': batch_results['errors']
        }
        
        return report
    
    def export_results(self, report: Dict, output_dir: str):
        """将所有结果导出到输出目录。"""
        os.makedirs(output_dir, exist_ok=True)
        
        # 导出主报告
        report_path = os.path.join(output_dir, 'comprehensive_report.json')
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        logger.info(f"主报告已保存到 {report_path}")
        
        # 导出分类数据
        classification_path = os.path.join(output_dir, 'classification_data.json')
        with open(classification_path, 'w', encoding='utf-8') as f:
            json.dump(report['classification_summary'], f, indent=2, ensure_ascii=False)
        logger.info(f"分类数据已保存到 {classification_path}")
        
        # 导出规则
        rules_path = os.path.join(output_dir, 'classification_rules.yaml')
        with open(rules_path, 'w', encoding='utf-8') as f:
            import yaml
            yaml.dump(report['rules']['yaml'], f, default_flow_style=False, allow_unicode=True)
        logger.info(f"分类规则已保存到 {rules_path}")
        
        gmail_rules_path = os.path.join(output_dir, 'gmail_rules.json')
        with open(gmail_rules_path, 'w', encoding='utf-8') as f:
            json.dump(report['rules']['gmail_labels'], f, indent=2, ensure_ascii=False)
        logger.info(f"Gmail 规则已保存到 {gmail_rules_path}")
        
        return {
            'report': report_path,
            'classification': classification_path,
            'rules': rules_path,
            'gmail_rules': gmail_rules_path
        }


def main():
    parser = argparse.ArgumentParser(
        description='批量邮件分类器 - 处理多个账户',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 处理配置中的所有账户
  python batch_classifier.py --config accounts.yaml
  
  # 使用自定义设置处理
  python batch_classifier.py --config accounts.yaml --days 14 --batch-size 50
  
  # 导出到特定目录
  python batch_classifier.py --config accounts.yaml --output-dir ./results
        """
    )
    
    parser.add_argument('--config', '-c', required=True, help='批量配置 YAML 路径')
    parser.add_argument('--days', type=int, default=7, help='分析天数（默认：7）')
    parser.add_argument('--batch-size', type=int, default=100, help='IMAP 批次大小（默认：100）')
    parser.add_argument('--output-dir', '-o', default='./output', help='输出目录')
    parser.add_argument('--verbose', '-v', action='store_true', help='启用详细日志')
    parser.add_argument('--skip-classification', action='store_true', 
                       help='跳过分类，仅获取邮件')
    parser.add_argument('--skip-rules', action='store_true', 
                       help='跳过规则生成')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # 验证配置
        if not os.path.exists(args.config):
            logger.error(f"未找到配置文件: {args.config}")
            sys.exit(1)
        
        # 初始化批量处理器
        processor = BatchClassifier(args.config)
        
        # 处理所有账户
        logger.info("开始批量邮件分类...")
        batch_results = processor.process_all_accounts(
            days=args.days,
            batch_size=args.batch_size
        )
        
        # 生成综合报告
        logger.info("正在生成综合报告...")
        report = processor.generate_comprehensive_report(batch_results)
        
        # 导出结果
        logger.info(f"正在导出结果到 {args.output_dir}")
        export_paths = processor.export_results(report, args.output_dir)
        
        # 打印摘要
        print("\n" + "="*70)
        print("批量分类完成")
        print("="*70)
        print(f"处理的账户数: {report['batch_summary']['total_accounts']}")
        print(f"成功: {report['batch_summary']['successful']}")
        print(f"失败: {report['batch_summary']['failed']}")
        print(f"总邮件数: {report['batch_summary']['total_emails_processed']}")
        
        if report['batch_summary']['total_emails_processed'] > 0:
            print(f"\n分类摘要:")
            class_summary = report['classification_summary']
            if 'summary' in class_summary:
                s = class_summary['summary']
                print(f"  日平均邮件数: {s.get('average_daily_emails', 0):.2f}")
                print(f"  低频账户: {s.get('low_frequency_count', 0)}")
        
        if report['errors']:
            print(f"\n遇到的错误:")
            for error in report['errors'][:3]:
                print(f"  - {error['account']}: {error['error'][:50]}...")
        
        print(f"\n输出文件:")
        for key, path in export_paths.items():
            print(f"  {key}: {path}")
        
        print("="*70)
        
    except KeyboardInterrupt:
        logger.info("\n批量处理已取消")
        sys.exit(1)
    except Exception as e:
        logger.error(f"致命错误: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

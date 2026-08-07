#!/usr/bin/env python3
"""
配置生成器 - 为邮件分类器创建示例配置文件
生成账户模板和自定义规则示例。
"""

import yaml
import argparse
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConfigGenerator:
    """生成配置文件的工具类。"""
    
    def __init__(self):
        self.templates = {
            'accounts': self._generate_accounts_template,
            'rules': self._generate_rules_template,
            'config': self._generate_main_config
        }
    
    def _generate_accounts_template(self) -> dict:
        """生成账户配置模板。"""
        return {
            'accounts': [
                {
                    'name': '工作',
                    'provider': 'gmail',  # gmail, outlook, lark, icloud
                    'email': 'your.work@gmail.com',
                    'imap_host': 'imap.gmail.com',
                    'imap_port': 993,
                    'auth_type': 'app_password',  # app_password 或 oauth
                    'password': 'your-app-password-here'
                },
                {
                    'name': '个人',
                    'provider': 'outlook',
                    'email': 'your.personal@outlook.com',
                    'imap_host': 'outlook.office365.com',
                    'imap_port': 993,
                    'auth_type': 'app_password',
                    'password': 'your-app-password-here'
                }
            ],
            'settings': {
                'low_frequency_threshold': 1.0,
                'classification_confidence': 0.7,
                'batch_size': 100
            }
        }
    
    def _generate_rules_template(self) -> dict:
        """生成自定义规则模板。"""
        return {
            'custom_categories': [
                {
                    'name': '重要客户',
                    'description': '来自 VIP 客户的邮件',
                    'weight': 1.5,
                    'keywords': ['发票', '合同', '法律通知', '紧急'],
                    'sender_domains': ['vip-client.com', 'enterprise.org'],
                    'subject_patterns': ['发票.*\\d{4}'],
                    'action': {
                        'label': '重要/客户',
                        'priority': '高',
                        'notify': True
                    }
                },
                {
                    'name': '家庭',
                    'description': '来自家人的个人邮件',
                    'weight': 1.2,
                    'keywords': ['爸爸', '妈妈', '哥哥', '姐姐', '生日'],
                    'action': {
                        'label': '家庭',
                        'priority': '高',
                        'notify': True
                    }
                }
            ]
        }
    
    def _generate_main_config(self) -> dict:
        """生成主配置文件。"""
        return {
            'version': '1.0',
            'description': '邮件分类器主配置',
            'settings': {
                'classification_confidence': 0.7,
                'analysis_days': 30,
                'low_frequency_threshold': 1.0,
                'enable_ml': False,
                'batch_size': 100,
                'cache_enabled': True,
                'cache_dir': '~/.email_classifier_cache'
            },
            'output': {
                'format': 'json',
                'include_raw_emails': True,
                'include_scores': True
            }
        }
    
    def generate_all(self, output_dir: str = '.'):
        """生成所有配置文件。"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        files_generated = []
        
        # 生成账户配置
        accounts_config = self._generate_accounts_template()
        accounts_path = output_path / 'accounts.yaml'
        with open(accounts_path, 'w', encoding='utf-8') as f:
            yaml.dump(accounts_config, f, default_flow_style=False, allow_unicode=True)
        files_generated.append(accounts_path)
        logger.info(f"账户配置已生成: {accounts_path}")
        
        # 生成自定义规则
        rules_config = self._generate_rules_template()
        rules_path = output_path / 'custom_rules.yaml'
        with open(rules_path, 'w', encoding='utf-8') as f:
            yaml.dump(rules_config, f, default_flow_style=False, allow_unicode=True)
        files_generated.append(rules_path)
        logger.info(f"自定义规则已生成: {rules_path}")
        
        # 生成主配置
        main_config = self._generate_main_config()
        main_path = output_path / 'config.yaml'
        with open(main_path, 'w', encoding='utf-8') as f:
            yaml.dump(main_config, f, default_flow_style=False, allow_unicode=True)
        files_generated.append(main_path)
        logger.info(f"主配置已生成: {main_path}")
        
        return files_generated


def main():
    parser = argparse.ArgumentParser(
        description='生成邮件分类器配置文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 生成所有配置文件
  python config_generator.py --all
  
  # 仅生成账户配置
  python config_generator.py --accounts
  
  # 生成到特定目录
  python config_generator.py --all --output-dir ./my_config
        """
    )
    
    parser.add_argument('--all', '-a', action='store_true', help='生成所有配置文件')
    parser.add_argument('--accounts', action='store_true', help='仅生成账户配置')
    parser.add_argument('--rules', action='store_true', help='仅生成自定义规则')
    parser.add_argument('--config', action='store_true', help='仅生成主配置')
    parser.add_argument('--output-dir', '-o', default='.', help='输出目录')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        generator = ConfigGenerator()
        files_generated = []
        
        if args.all or args.accounts:
            files_generated.extend(generator.generate_all(args.output_dir))
        
        if args.all or args.rules:
            output_path = Path(args.output_dir)
            rules_config = generator._generate_rules_template()
            rules_path = output_path / 'custom_rules.yaml'
            with open(rules_path, 'w', encoding='utf-8') as f:
                yaml.dump(rules_config, f, default_flow_style=False, allow_unicode=True)
            files_generated.append(rules_path)
            logger.info(f"自定义规则已生成: {rules_path}")
        
        if args.all or args.config:
            output_path = Path(args.output_dir)
            main_config = generator._generate_main_config()
            main_path = output_path / 'config.yaml'
            with open(main_path, 'w', encoding='utf-8') as f:
                yaml.dump(main_config, f, default_flow_style=False, allow_unicode=True)
            files_generated.append(main_path)
            logger.info(f"主配置已生成: {main_path}")
        
        print(f"\n已生成 {len(files_generated)} 个配置文件:")
        for f in files_generated:
            print(f"  • {f}")
        
    except Exception as e:
        logger.error(f"生成配置失败: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

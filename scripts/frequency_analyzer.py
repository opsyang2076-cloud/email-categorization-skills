#!/usr/bin/env python3
"""
频率分析器 - 分析电子邮件账户参与模式
识别低频账户并提供建议。
"""

import json
import argparse
import logging
from datetime import datetime
from collections import Counter, defaultdict
from typing import Dict, List, Optional

# 可视化可选导入
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    plt = None

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    np = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FrequencyAnalyzer:
    """分析跨账户的邮件频率模式。"""
    
    # 频率级别定义
    FREQUENCY_LEVELS = {
        "daily_high": {"min": 10, "max": float('inf'), "label": "每日高频"},
        "daily_medium": {"min": 1, "max": 9, "label": "每日中频"},
        "daily_low": {"min": 0.1, "max": 0.9, "label": "每日低频"},
        "weekly_sporadic": {"min": 0, "max": 0.09, "label": "每周零星"}
    }
    
    def __init__(self, low_threshold: float = 1.0):
        """使用自定义阈值初始化分析器。"""
        self.low_threshold = low_threshold
        
    def analyze_account(self, account_data: Dict) -> Dict:
        """分析单个账户的邮件频率。"""
        emails = account_data.get('emails', [])
        
        if not emails:
            return self._empty_analysis(account_data.get('name', '未知'))
        
        # 解析日期
        date_counts = Counter()
        for email in emails:
            date_str = email.get('date', '')
            try:
                date = datetime.fromisoformat(date_str)
                date_key = date.strftime('%Y-%m-%d')
                date_counts[date_key] += 1
            except:
                continue
        
        # 计算指标
        total_emails = len(emails)
        unique_days = len(date_counts)
        if date_counts:
            # 解析日期为 datetime 对象进行比较
            parsed_dates = []
            for date_str in date_counts.keys():
                try:
                    parsed_dates.append(datetime.fromisoformat(date_str))
                except:
                    continue
            if parsed_dates:
                date_range_days = max(1, (max(parsed_dates) - min(parsed_dates)).days)
            else:
                date_range_days = 1
        else:
            date_range_days = 1
        daily_average = total_emails / max(unique_days, 1)
        
        # 确定频率级别
        frequency_level = self._classify_frequency(daily_average)
        
        # 生成建议
        recommendation = self._generate_recommendation(
            frequency_level,
            daily_average,
            total_emails,
            account_data.get('name', '')
        )
        
        return {
            'account_name': account_data.get('name', '未知'),
            'email_address': account_data.get('email_address', ''),
            'total_emails': total_emails,
            'unique_days': unique_days,
            'date_range_days': date_range_days,
            'daily_average': round(daily_average, 2),
            'frequency_level': frequency_level,
            'frequency_label': self.FREQUENCY_LEVELS[frequency_level]['label'],
            'recommendation': recommendation,
            'is_low_frequency': daily_average < self.low_threshold,
            'date_distribution': dict(sorted(date_counts.items()))
        }
    
    def _classify_frequency(self, daily_avg: float) -> str:
        """将日平均数分类为频率级别。"""
        for level, ranges in self.FREQUENCY_LEVELS.items():
            if ranges['min'] <= daily_avg <= ranges['max']:
                return level
        return 'daily_low'
    
    def _generate_recommendation(self, level: str, daily_avg: float,
                                  total: int, account_name: str) -> str:
        """根据频率生成可行的建议。"""
        recommendations = {
            "daily_high": [
                "高参与账户。考虑设置邮件过滤器。",
                "活跃账户 - 确保不会错过重要邮件。",
                "考虑使用标签/文件夹进行更好的组织。"
            ],
            "daily_medium": [
                "常规参与 - 良好的平衡。",
                "考虑每天检查此账户。",
                "标准监控频率是合适的。"
            ],
            "daily_low": [
                f"低参与（每天 {daily_avg:.2f} 封邮件）。",
                "考虑每周检查而不是每天。",
                "归档旧邮件以减少杂乱。"
            ],
            "weekly_sporadic": [
                f"极低参与（每天 {daily_avg:.2f} 封邮件）。",
                "考虑取消订阅非必需邮件。",
                "归档此账户或设置转发到主收件箱。",
                "审查此账户是否仍然需要。"
            ]
        }
        
        # 选择合适的建议
        recs = recommendations.get(level, recommendations["daily_low"])
        
        # 添加账户特定建议
        if daily_avg < 0.1 and total > 0:
            recs.append(f"考虑归档 {account_name} 的旧邮件。")
        
        return " ".join(recs[:2])  # 返回前 2 条建议
    
    def _empty_analysis(self, account_name: str) -> Dict:
        """为没有邮件的账户返回空分析。"""
        return {
            'account_name': account_name,
            'email_address': '',
            'total_emails': 0,
            'unique_days': 0,
            'date_range_days': 0,
            'daily_average': 0,
            'frequency_level': 'no_data',
            'frequency_label': '无数据',
            'recommendation': '无邮件可分析',
            'is_low_frequency': False,
            'date_distribution': {}
        }
    
    def analyze_all_accounts(self, classification_data: Dict) -> Dict:
        """分析分类数据中所有账户的频率。"""
        results = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_accounts': len(classification_data.get('account_summaries', {})),
                'low_frequency_count': 0
            },
            'accounts': {},
            'low_frequency_accounts': [],
            'summary': {}
        }
        
        for account_name, account_data in classification_data.get('account_summaries', {}).items():
            # 获取此账户的邮件
            emails = classification_data.get('results', {}).get(account_name, {}).get('emails', [])
            
            account_info = {
                'name': account_name,
                'email_address': classification_data.get('results', {}).get(account_name, {}).get('email_address', ''),
                'emails': emails
            }
            
            analysis = self.analyze_account(account_info)
            results['accounts'][account_name] = analysis
            
            if analysis['is_low_frequency']:
                results['low_frequency_accounts'].append(analysis)
                results['metadata']['low_frequency_count'] += 1
        
        # 生成统计摘要
        all_dailies = [a['daily_average'] for a in results['accounts'].values()]
        if all_dailies:
            summary_data = {
                'average_daily_emails': round(sum(all_dailies) / len(all_dailies), 2),
                'high_frequency_count': sum(1 for d in all_dailies if d >= 10),
                'medium_frequency_count': sum(1 for d in all_dailies if 1 <= d < 10),
                'low_frequency_count': sum(1 for d in all_dailies if d < 1),
                'total_accounts': len(all_dailies)
            }
            # 如果 numpy 可用，添加中位数
            if NUMPY_AVAILABLE:
                summary_data['median_daily_emails'] = round(float(np.median(all_dailies)), 2)
            else:
                # 手动计算中位数
                sorted_dailies = sorted(all_dailies)
                n = len(sorted_dailies)
                if n % 2 == 0:
                    summary_data['median_daily_emails'] = round((sorted_dailies[n//2-1] + sorted_dailies[n//2]) / 2, 2)
                else:
                    summary_data['median_daily_emails'] = round(sorted_dailies[n//2], 2)
            results['summary'] = summary_data
        
        return results
    
    def generate_visualization(self, analysis: Dict, output_path: str = 'frequency_chart.png'):
        """生成频率分布图表。"""
        if not MATPLOTLIB_AVAILABLE:
            logger.warning("matplotlib 不可用，跳过可视化")
            return False
        
        try:
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            
            # 1. 日平均分布
            ax1 = axes[0, 0]
            accounts = list(analysis['accounts'].keys())
            dailies = [analysis['accounts'][a]['daily_average'] for a in accounts]
            colors = ['red' if analysis['accounts'][a]['is_low_frequency'] else 'green' 
                     for a in accounts]
            ax1.barh(accounts, dailies, color=colors)
            ax1.axvline(x=self.low_threshold, color='orange', linestyle='--', 
                       label=f'低频阈值（{self.low_threshold}封/天）')
            ax1.set_xlabel('日平均邮件数')
            ax1.set_title('各账户邮件频率')
            ax1.legend()
            
            # 2. 频率级别分布
            ax2 = axes[0, 1]
            level_counts = Counter(a['frequency_level'] for a in analysis['accounts'].values())
            if MATPLOTLIB_AVAILABLE and hasattr(ax2, 'pie'):
                ax2.pie(level_counts.values(), labels=level_counts.keys(), autopct='%1.1f%%')
            ax2.set_title('频率级别分布')
            
            # 3. 顶级账户的时间序列
            ax3 = axes[1, 0]
            top_accounts = sorted(analysis['accounts'].keys(),
                                key=lambda x: analysis['accounts'][x]['total_emails'],
                                reverse=True)[:3]
            for account in top_accounts:
                dist = analysis['accounts'][account]['date_distribution']
                if dist:
                    dates = list(dist.keys())
                    counts = list(dist.values())
                    if MATPLOTLIB_AVAILABLE and hasattr(ax3, 'plot'):
                        ax3.plot(dates, counts, marker='o', label=account)
            ax3.set_xlabel('日期')
            ax3.set_ylabel('每日邮件数')
            ax3.set_title('邮件趋势（顶级账户）')
            if MATPLOTLIB_AVAILABLE and hasattr(ax3, 'legend'):
                ax3.legend()
            
            # 4. 统计摘要
            ax4 = axes[1, 1]
            summary = analysis.get('summary', {})
            if summary:
                metrics = [
                    f"总账户数: {summary.get('total_accounts', 0)}",
                    f"日平均: {summary.get('average_daily_emails', 0)}",
                    f"低频: {summary.get('low_frequency_count', 0)}",
                    f"中频: {summary.get('medium_frequency_count', 0)}",
                    f"高频: {summary.get('high_frequency_count', 0)}"
                ]
                ax4.text(0.1, 0.5, '\n'.join(metrics), fontsize=12, 
                        verticalalignment='center', transform=ax4.transAxes)
                ax4.axis('off')
                ax4.set_title('统计摘要')
            
            plt.tight_layout()
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            logger.info(f"可视化已保存到 {output_path}")
            plt.close()
            
            return True
            
        except Exception as e:
            logger.error(f"生成可视化失败: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description='邮件频率分析器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 从分类数据中分析频率
  python frequency_analyzer.py --input classified_emails.json --output frequency_report.json
  
  # 设置自定义阈值
  python frequency_analyzer.py --input classified_emails.json --threshold 0.5
  
  # 生成可视化
  python frequency_analyzer.py --input classified_emails.json --visualize
        """
    )
    
    parser.add_argument('--input', '-i', required=True, help='输入分类 JSON 文件')
    parser.add_argument('--output', '-o', help='输出报告 JSON 文件')
    parser.add_argument('--threshold', type=float, default=1.0, 
                       help='低频阈值（默认：每天 1.0 封邮件）')
    parser.add_argument('--visualize', action='store_true', help='生成频率图表')
    parser.add_argument('--output-chart', default='frequency_chart.png', 
                       help='图表输出路径（默认：frequency_chart.png）')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # 加载分类数据
        with open(args.input, 'r', encoding='utf-8') as f:
            classification_data = json.load(f)
        
        # 初始化分析器
        analyzer = FrequencyAnalyzer(low_threshold=args.threshold)
        
        # 分析所有账户
        analysis = analyzer.analyze_all_accounts(classification_data)
        
        # 保存输出
        output_path = args.output or 'frequency_report.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        logger.info(f"频率分析已保存到 {output_path}")
        
        # 打印摘要
        print("\n" + "="*60)
        print("频率分析摘要")
        print("="*60)
        print(f"分析的总账户数: {analysis['metadata']['total_accounts']}")
        print(f"低频账户数: {analysis['metadata']['low_frequency_count']}")
        
        if analysis.get('summary'):
            s = analysis['summary']
            print(f"\n统计数据:")
            print(f"  日平均邮件数: {s.get('average_daily_emails', 0)}")
            print(f"  中位数日邮件数: {s.get('median_daily_emails', 0)}")
            print(f"  高频账户: {s.get('high_frequency_count', 0)}")
            print(f"  中频账户: {s.get('medium_frequency_count', 0)}")
            print(f"  低频账户: {s.get('low_frequency_count', 0)}")
        
        if analysis['low_frequency_accounts']:
            print(f"\n需要关注的低频账户:")
            for account in analysis['low_frequency_accounts'][:5]:
                print(f"  • {account['account_name']}: {account['daily_average']:.2f} 封/天")
                print(f"    建议: {account['recommendation'][:80]}...")
        
        print("="*60)
        
        # 如果需要，生成可视化
        if args.visualize:
            chart_path = args.output_chart
            if analyzer.generate_visualization(analysis, chart_path):
                print(f"\n频率图表已保存到: {chart_path}")
        
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
